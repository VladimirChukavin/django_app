from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    """
    Create products
    """

    def handle(self, *args, **options):
        products_names = [
            "Laptop",
            "Desktop",
            "Smartphone",
        ]
        for name in products_names:
            product, created = Product.objects.get_or_create(name=name)
            self.stdout.write(f"Created product: {product.name}")
        self.stdout.write(self.style.SUCCESS("Successfully created products"))
