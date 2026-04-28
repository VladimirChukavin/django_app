from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Start demo bulk actions"))

        # info = [
        #     ("gadget 1", 199),
        #     ("gadget 2", 280),
        #     ("gadget 3", 350),
        # ]
        # products = [Product(name=name, price=price) for name, price in info]
        #
        # result = Product.objects.bulk_create(products)
        # for obj in result:
        #     print(obj)

        result = Product.objects.filter(name__contains="gadget").update(discount=10)
        print(result)

        self.stdout.write(self.style.SUCCESS("Successfully bulk actions"))
