from django.urls import path
from django.views.generic import RedirectView

from .views import (
    CancelView,
    ItemCheckoutView,
    ItemsListView,
    OrderCheckoutView,
    OrdersListView,
    SuccessView,
    get_stripe_session_id_for_item,
    get_stripe_session_id_for_order,
)

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="items_list")),
    path("items/", ItemsListView.as_view(), name="items_list"),
    path("item/<int:id>/", ItemCheckoutView.as_view(), name="item_detail"),
    path(
        "buy/<int:item_id>/",
        get_stripe_session_id_for_item,
        name="buy_item",
    ),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("order/<int:id>/", OrderCheckoutView.as_view(), name="order_detail"),
    path(
        "buy_order/<int:order_id>/",
        get_stripe_session_id_for_order,
        name="buy_order",
    ),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("success/", SuccessView.as_view(), name="success"),
]
