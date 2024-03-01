from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView, list

import stripe

from stripe_shop.settings import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY

from .models import Item, Order
from .utils import create_stripe_session

stripe.api_key = STRIPE_SECRET_KEY
public_key = STRIPE_PUBLISHABLE_KEY


def get_stripe_session_id_for_order(request, order_id):
    """Получает идентификатор сеанса Stripe для оформления заказа."""
    order = get_object_or_404(Order, id=order_id)

    discounts = []
    if order.discount:
        discounts = [{"coupon": order.discount.stripe_coupon_id}]

    line_items = [
        {
            "price_data": {
                "currency": item.currency.lower(),
                "product_data": {"name": item.name},
                "unit_amount": int(item.price * 100),
            },
            "quantity": 1,
        }
        for item in order.items.all()
    ]

    if order.tax:
        for item in line_items:
            item["tax_rates"] = [order.tax.stripe_tax_id]

    return JsonResponse(create_stripe_session(line_items, discounts))


def get_stripe_session_id_for_item(request, item_id):
    """Получает идентификатор сеанса Stripe для оформления покупки товара."""
    item = get_object_or_404(Item, id=item_id)

    line_items = [
        {
            "price_data": {
                "currency": item.currency.lower(),
                "product_data": {"name": item.name},
                "unit_amount": int(item.price * 100),
            },
            "quantity": 1,
        }
    ]

    return JsonResponse(create_stripe_session(line_items))


class ItemsListView(list.ListView):
    """Отображение списка заказов."""

    model = Item
    template_name = "stripe/items_list.html"
    context_object_name = "items"


class OrdersListView(list.ListView):
    """Отображение списка заказов."""

    model = Order
    template_name = "stripe/orders_list.html"
    context_object_name = "orders"


class ItemCheckoutView(View):
    """Отображение страницы оформления заказа для товара."""

    template_name = "stripe/item_checkout.html"

    def get(self, request, id):
        item = get_object_or_404(Item, id=id)
        return render(
            request,
            self.template_name,
            {"item": item, "public_key": public_key},
        )


class OrderCheckoutView(View):
    """Отображение страницы оформления заказа."""

    template_name = "stripe/order_checkout.html"

    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        return render(
            request,
            self.template_name,
            {"order": order, "public_key": public_key},
        )


class SuccessView(TemplateView):
    """Отображение страницы успешного оформления заказа."""

    template_name = "stripe/success.html"


class CancelView(TemplateView):
    """Отображение страницы отмены заказа."""

    template_name = "stripe/cancel.html"
