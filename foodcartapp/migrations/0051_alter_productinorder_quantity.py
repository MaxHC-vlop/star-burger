# Generated by Django 3.2.15 on 2023-03-07 16:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0050_auto_20230307_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinorder',
            name='quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
    ]