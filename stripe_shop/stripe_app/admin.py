from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Discount, Item, Order, Tax


class OrderAdminForm(forms.ModelForm):
    """Форма для администрирования заказов."""

    class Meta:
        model = Order
        fields = "__all__"

    def clean_items(self):
        """Проверка, чтобы все товары в заказе были в одной валюте."""
        items = self.cleaned_data.get("items")

        if items:
            currencies = set(item.currency for item in items.all())
            if len(currencies) > 1:
                raise ValidationError(
                    "Все товары в заказе должны быть в одной валюте."
                )
        return items


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Административная панель для модели Item."""

    list_display = ("name", "description", "price", "currency")
    search_fields = ("name",)
    list_filter = ("currency",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Административная панель для модели Order."""

    form = OrderAdminForm
    filter_horizontal = ("items",)
    list_display = (
        "id",
        "created_at",
        "total_price_display",
    )
    search_fields = ("id",)

    @admin.display(description="Итоговая цена без учета скидки и налога")
    def total_price_display(self, obj):
        return obj.total_price


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    """Административная панель для модели Tax."""

    list_display = ("tax_name", "percentage")
    search_fields = ("tax_name",)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Административная панель для модели Discount."""

    list_display = ("stripe_coupon_id", "percent_off")
    search_fields = ("stripe_coupon_id",)
