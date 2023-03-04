from geopy import distance
from django import forms
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from requests import RequestException

from foodcartapp.models import Product, Restaurant
from foodcartapp.models import Order
from places.models import Place
from places.fetch_place import get_place, fetch_coordinates


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {
            item.restaurant_id:
            item.availability for item in product.menu_items.all()
        }
        ordered_availability = [
            availability.get(restaurant.id, False) for restaurant in restaurants
        ]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    yandex_api_key = settings.YANDEX_API_KEY

    orders = Order.objects.all() \
        .with_price().get_restaurants()
    order_places = [order.address for order in orders]
    places = Place.objects.filter(address__in=order_places)

    for order in orders:
        if order.address not in places.values_list('address', flat=True):
            try:
                place = get_place(yandex_api_key, order.address)
            except RequestException:
                order.restaurant_distances = None
                continue

        for place_db in places:
            if place_db.address == order.address:
                place = place_db

        for restaurant in order.restaurants:
            if not restaurant.longitude or not restaurant.latitude:
                try:
                    restaurant_coordinates = fetch_coordinates(
                        yandex_api_key, restaurant.address
                    )
                except request.RequestException:
                    order.restaurant_distances = None
                    continue

                restaurant.longitude, restaurant.latitude = restaurant_coordinates
                restaurant.save()

            restaurant_distance = distance.distance(
                (restaurant.latitude, restaurant.longitude),
                (place.latitude, place.longitude)
            ).km
            order.restaurant_distances.append(
                (restaurant.name, round(restaurant_distance, 2))
            )
            order.restaurant_distances = sorted(
                order.restaurant_distances,
                key=lambda rest_dist: rest_dist[1]
            )

    return render(
        request, template_name='order_items.html',
        context={'orders': orders}
        )
