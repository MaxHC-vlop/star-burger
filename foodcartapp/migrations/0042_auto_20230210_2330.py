# Generated by Django 3.2.15 on 2023-02-10 23:30

from django.db import migrations


def set_price(apps, schema_editor):
    ProductInOrder = apps.get_model('foodcartapp', 'ProductInOrder')
    Product = apps.get_model('foodcartapp', 'Product')

    products = Product.objects.all()
    for product in products.iterator():
        ProductInOrder.objects.filter(product=product) \
            .update(price=product.price)


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_productinorder_price'),
    ]

    operations = [
        migrations.RunPython(set_price),
    ]
