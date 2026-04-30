from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Start demo select fields"))

        # products_values = Product.objects.values("pk", "name")
        #
        # for value in products_values:
        #     print(value)

        users_info = User.objects.values_list("username", flat=True)
        print(list(users_info))
        for user in users_info:
            print(user)

        self.stdout.write(self.style.SUCCESS("Successfully created orders"))
