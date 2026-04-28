from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from shopapp.models import Order, Product


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        # with transaction.atomic():
        #     ...

        self.stdout.write(f"Created order with products")

        user = User.objects.get(username="admin")
        # products: Sequence[Product] = Product.objects.all()
        # products: Sequence[Product] = Product.objects.defer(
        #     "description", "price", "created_at"
        # ).all()
        products: Sequence[Product] = Product.objects.only("pk").all()
        order, created = Order.objects.get_or_create(
            # delivery_address="Lenin street, 2",
            # promocode="SALE123",
            delivery_address="South-green street, 8",
            promocode="VIP123",
            user=user,
        )

        for product in products:
            order.products.add(product)

        order.save()

        self.stdout.write(f"Created order: #{order}")
        self.stdout.write(self.style.SUCCESS("Successfully created orders"))
