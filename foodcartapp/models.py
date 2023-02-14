from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import F, Sum
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def with_price(self):
        price = self.prefetch_related('item_products') \
            .annotate(
                price=Sum(
                    F('item_products__price') * F('item_products__quantity')
                )
            )

        return price


class Order(models.Model):
    RAW = 'Необработанный'
    PREPARE = 'Готовится'
    SENT = 'Отправлен'
    COMPLETED = 'Выполнен'
    STATUS_CHOICES = (
        (RAW, RAW),
        (PREPARE, PREPARE),
        (SENT, SENT),
        (COMPLETED, COMPLETED)
    )

    CASH = 'Наличностью'
    ELECTRONIC_MONEY = 'Электронно'
    PAYMENT_CHOICES = (
        (CASH, CASH),
        (ELECTRONIC_MONEY, ELECTRONIC_MONEY)
    )

    firstname = models.CharField(
        max_length=20,
        verbose_name='Имя'
    )
    lastname = models.CharField(
        max_length=20,
        verbose_name='Фамилия'
    )
    phonenumber = PhoneNumberField(
        verbose_name='Номер телефона',
    )
    address = models.CharField(
        max_length=100,
        verbose_name='Адрес'
    )
    status = models.CharField(
        verbose_name='Статус заказа',
        max_length=14,
        choices=STATUS_CHOICES,
        default=RAW,
        db_index=True
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        db_index=True
    )
    registrated_at = models.DateTimeField(
        verbose_name='Зарегистрирован',
        db_index=True,
        default=timezone.now
    )
    called_at = models.DateTimeField(
        verbose_name='Звонок заказчику',
        db_index=True,
        blank=True,
        null=True
    )
    delivered_at = models.DateTimeField(
        verbose_name='Доставлен',
        db_index=True,
        blank=True,
        null=True
    )
    payment_method = models.CharField(
        verbose_name='Способо оплаты',
        max_length=14,
        choices=PAYMENT_CHOICES,
        default=CASH,
        db_index=True
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.pk} {self.firstname} - {self.phonenumber}"


class ProductInOrder(models.Model):
    product = models.ForeignKey(
        'Product',
        verbose_name='Продукт',
        related_name='orders',
        on_delete=models.CASCADE,
        db_index=True
        )
    order = models.ForeignKey(
        'Order',
        verbose_name='Заказ',
        related_name='item_products',
        on_delete=models.CASCADE,
        db_index=True
        )
    quantity = models.PositiveIntegerField(
        'Количество'
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Продукт в заказе'
        verbose_name_plural = 'Продукты в заказе'

    def __str__(self):
        order = f'Заказ {self.order.pk}, {self.product} ({self.quantity} шт.) по {self.price} руб.'
        return order
