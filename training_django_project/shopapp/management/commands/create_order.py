from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(username="admin")
        order = Order.objects.get_or_create(
            delivery_address="Lenin street, 2",
            promocode="SALE123",
            user=user,
        )
        self.stdout.write(f"Created order: #{order}")
        self.stdout.write(self.style.SUCCESS("Successfully created orders"))
