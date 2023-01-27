import json

import phonenumbers

from django.http import JsonResponse
from django.templatetags.static import static
from .models import Product
from .models import Order
from .models import ProductInOrder


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def register_order(request):
    try:
        data = json.loads(request.body.decode())
        user_phonenumber = phonenumbers.parse(data['phonenumber'], 'RU')
        if phonenumbers.is_valid_number_for_region(user_phonenumber, 'RU'):
            phonenumber = f'+{user_phonenumber.country_code}{user_phonenumber.national_number}'
            order = Order.objects.create(
                firstname=data['firstname'],
                lastname=data['lastname'],
                phonenumber=phonenumber,
                address=data['address']
            )
            for product in data['products']:
                ProductInOrder.objects.create(
                    order=order,
                    product=Product.objects.get(pk=product['product']),
                    quantity=product['quantity'],
                )
    except ValueError:
        return JsonResponse({
            'ValueError': 'bad value',
        })
    return JsonResponse({})
