from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db.models import Avg, Max, Min, Count, Sum

from shopapp.models import Product, Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Start demo aggregate"))

        # result = Product.objects.filter(name__contains="gadget").aggregate(
        #     avg_price=Avg("price"),
        #     max_price=Max("price"),
        #     min_price=Min("price"),
        #     count=Count("pk"),
        # )
        # print(result)

        orders = Order.objects.annotate(
            total=Sum("products__price", default=0),
            products_count=Count("products"),
        )
        for order in orders:
            print(
                f"Order #{order.pk}, count {order.products_count}, total: ${round(order.total, 2)}"
            )

        self.stdout.write(self.style.SUCCESS("Successfully aggregate"))
