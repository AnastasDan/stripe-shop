from django.core.management.base import BaseCommand
from django.db import transaction

import stripe

from stripe_app.constants import DEFAULT_TAX_PERCENTAGE
from stripe_app.models import Tax
from stripe_shop.settings import STRIPE_SECRET_KEY


class Command(BaseCommand):
    """Команда для создания дефолтного налога при запуске проекта."""

    help = "Создание налога при запуске проекта"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        """Обработчик команды для создания налога."""
        try:
            stripe.api_key = STRIPE_SECRET_KEY
            sales_tax = stripe.TaxRate.create(
                display_name="Test tax", inclusive=False, percentage=7
            )

            if not Tax.objects.filter(stripe_tax_id=sales_tax.id).exists():
                Tax.objects.create(
                    stripe_tax_id=sales_tax.id,
                    tax_name="Test tax",
                    percentage=DEFAULT_TAX_PERCENTAGE,
                )
                self.stdout.write(
                    self.style.SUCCESS("Налог успешно добавлен.")
                )
            else:
                self.stdout.write(self.style.WARNING("Налог уже существует."))

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Ошибка при добавлении налога: {str(e)}")
            )
