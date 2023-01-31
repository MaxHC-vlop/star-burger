from types import NoneType

import phonenumbers

from django.http import JsonResponse
from django.templatetags.static import static
from .models import Product
from .models import Order
from .models import ProductInOrder
from rest_framework.decorators import api_view
from rest_framework.response import Response


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


@api_view(['POST'])
def register_order(request):
    data = request.data
    try:
        products = data['products']

    except KeyError:
        return Response(
            {'error': 'products key not presented or not list'}, status=400
        )

    if isinstance(products, str):
        return Response({
            'error': 'product key cannot be a string'}, status=400
        )

    if isinstance(products, NoneType):
        return Response({
            'error': 'product key cannot be missing'}, status=400
        )

    if not products:
        return Response({
            'error': 'products cart is empty'}, status=400
        )

    try:
        firstname = data['firstname']
        lastname = data['lastname']
        address = data['address']
        if not firstname:
            return Response(['firstname'], status=400)

        if not isinstance(firstname, str):
            return Response(['not str'], status=400)

        if not lastname:
            return Response(['lastname'], status=400)

        if not address:
            return Response(['address'], status=400)

        phonenumber = phonenumbers.parse(data['phonenumber'], 'RU')

    except KeyError:
        return Response(
            {'error': 'order keys not presented'}, status=400
        )

    except phonenumbers.NumberParseException:
        return Response(
            {'error': 'phonenumber'}, status=400
        )

    is_valid_phonenumber = phonenumbers.is_valid_number_for_region(
        phonenumber, 'RU'
    )
    if not is_valid_phonenumber:
        return Response({'error': 'wrong phone number'}, status=400)

    valid_phonenumber = f'+{phonenumber.country_code}{phonenumber.national_number}'
    order = Order.objects.create(
        firstname=data['firstname'],
        lastname=data['lastname'],
        phonenumber=valid_phonenumber,
        address=data['address']
    )
    for product in data['products']:
        try:
            product = Product.objects.get(pk=product['product'])

        except Product.DoesNotExist:
            return Response({'error': 'not pk'}, status=400)

        ProductInOrder.objects.create(
            order=order,
            product=product,
            quantity=product['quantity'],
            )

    return Response(['Success order!'], status=200)
