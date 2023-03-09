import phonenumbers

from phonenumber_field import serializerfields
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


class OrderSerializer(serializers.ModelSerializer):
    products = ProductInOrderSerializer(
        many=True,
        allow_empty=False,
        write_only=True
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

    def create(self, validated_data):
        order = Order.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber'],
            address=validated_data['address']
        )

        return order
