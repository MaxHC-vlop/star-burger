# Generated by Django 3.2.15 on 2023-02-13 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, db_index=True, verbose_name='Комментарий'),
        ),
    ]
