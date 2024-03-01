from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import (
    MAX_CURRENCY_LENGTH,
    MAX_DISCOUNT_PERCENT,
    MAX_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PERCENTAGE,
    MIN_DEFAULT_PRICE,
    MIN_DISCOUNT_PERCENT,
    MIN_PERCENTAGE,
    RUB,
    USD,
)


class Item(models.Model):
    """Модель для товара."""

    CURRENCY_CHOICES = (
        (USD, "Доллар США"),
        (RUB, "Российский рубль"),
    )

    name = models.CharField("Наименование", max_length=MAX_NAME_LENGTH)
    description = models.TextField("Описание", max_length=MAX_LENGTH)
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
        default=MIN_DEFAULT_PRICE,
        validators=[MinValueValidator(MIN_DEFAULT_PRICE)],
    )
    currency = models.CharField(
        "Валюта",
        max_length=MAX_CURRENCY_LENGTH,
        choices=CURRENCY_CHOICES,
        default=RUB,
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("-id",)

    def __str__(self):
        """Метод возвращает строковое представление объекта."""
        return self.name


class Order(models.Model):
    """Модель для заказа."""

    items = models.ManyToManyField(Item, verbose_name="Товары")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    discount = models.ForeignKey(
        "Discount",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Скидка",
    )
    tax = models.ForeignKey(
        "Tax",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Налог",
    )

    def __str__(self):
        """Метод возвращает строковое представление объекта."""
        return f"Заказ #{self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("-created_at",)

    @property
    def total_price(self):
        """Получение общей стоимости с учетом скидки и налога."""
        return sum(item.price for item in self.items.all())


class Tax(models.Model):
    """Модель для налога."""

    stripe_tax_id = models.CharField(
        "Идентификатор налога Stripe", max_length=MAX_LENGTH, unique=True
    )
    tax_name = models.CharField(
        "Наименование налога", max_length=MAX_NAME_LENGTH, unique=True
    )
    percentage = models.PositiveIntegerField(
        "Процент налога",
        validators=[
            MinValueValidator(MIN_PERCENTAGE),
            MaxValueValidator(MAX_PERCENTAGE),
        ],
    )

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"
        ordering = ("-id",)

    def __str__(self):
        """Метод возвращает строковое представление объекта."""
        return self.tax_name


class Discount(models.Model):
    """Модель для скидки."""

    stripe_coupon_id = models.CharField(
        "Идентификатор купона Stripe", max_length=MAX_LENGTH, unique=True
    )
    percent_off = models.FloatField(
        "Скидка в процентах",
        validators=[
            MinValueValidator(MIN_DISCOUNT_PERCENT),
            MaxValueValidator(MAX_DISCOUNT_PERCENT),
        ],
    )

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"
        ordering = ("-id",)

    def __str__(self):
        """Метод возвращает строковое представление объекта."""
        return self.stripe_coupon_id
