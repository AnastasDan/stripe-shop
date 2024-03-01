from django.core.management.base import BaseCommand
from django.db import transaction

import stripe

from stripe_app.constants import DEFAULT_PERCENT_OFF
from stripe_app.models import Discount
from stripe_shop.settings import STRIPE_SECRET_KEY


class Command(BaseCommand):
    """Команда для создания дефолтной скидки при запуске проекта."""

    help = "Создание скидки при запуске проекта"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        try:
            stripe.api_key = STRIPE_SECRET_KEY
            percent_coupon = stripe.Coupon.create(
                percent_off=DEFAULT_PERCENT_OFF
            )

            if not Discount.objects.filter(
                stripe_coupon_id=percent_coupon.id
            ).exists():
                Discount.objects.create(
                    stripe_coupon_id=percent_coupon.id,
                    percent_off=DEFAULT_PERCENT_OFF,
                )
                self.stdout.write(
                    self.style.SUCCESS("Купон успешно добавлен.")
                )
            else:
                self.stdout.write(self.style.WARNING("Купон уже существует."))

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Ошибка при добавлении купона: {str(e)}")
            )
