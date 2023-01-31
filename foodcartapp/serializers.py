import phonenumbers

from foodcartapp.models import Product
from foodcartapp.models import Order
from foodcartapp.models import ProductInOrder
from rest_framework import serializers


class ProductInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInOrder
        fields = [
            'product',
            'quantity'
        ]

    def validate_products(self, value):
        for product in value:
            key = product['product']
            try:
                Product.objects.get(pk=key)

            except Product.DoesNotExist:
                raise serializers.ValidationError(f'Недопустимый первичный ключ {key}.')

        return value


class OrderSerializer(serializers.ModelSerializer):
    products = ProductInOrderSerializer(
        many=True,
        allow_empty=False,
    )

    class Meta:
        model = Order
        fields = [
            'firstname',
            'lastname',
            'phonenumber',
            'address',
            'products'
        ]

    def validate_phonenumber(self, value):
        phonenumber = phonenumbers.parse(value, 'RU')
        valid_phonenumber = phonenumbers.is_valid_number_for_region(
            phonenumber, 'RU'
        )
        if not valid_phonenumber:
            raise serializers.ValidationError('Введен некорректный номер телефона.')

        return value
