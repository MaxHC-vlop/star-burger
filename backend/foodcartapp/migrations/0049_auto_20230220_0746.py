# Generated by Django 3.2.15 on 2023-02-20 07:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_auto_20230218_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='latitude',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(-90), django.core.validators.MinValueValidator(90)], verbose_name='Широта'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='longitude',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(-180), django.core.validators.MinValueValidator(180)], verbose_name='Долгота'),
        ),
    ]
