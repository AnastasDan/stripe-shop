from django.apps import AppConfig


class StripeAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stripe_app"
    verbose_name = "Платежная система Stripe"
