from string import ascii_letters
from random import choices

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from .utils import add_two_numbers
from .models import Product, Order


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(3, 5)
        self.assertEqual(result, 8)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_product_create_view(self):
        response = self.client.post(
            reverse("shopapp:create_product"),
            {
                # "name": "Table",
                "name": self.product_name,
                "price": "123.45",
                "description": "This is a table",
                "discount": "5",
            },
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Something")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.product.delete()

    def test_product_details_view(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = ["product-fixtures.json"]

    def test_get_products_list(self):
        response = self.client.get(reverse("shopapp:products_list"))

        # for product in Product.objects.filter(archived=False).all():
        #     self.assertContains(response, product.name)

        # products = Product.objects.filter(archived=False).all()
        # products_ = response.context["products"]

        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)

        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, "shopapp/products_list.html")


class ProductsExportViewTestCase(TestCase):
    fixtures = ["product-fixtures.json"]

    def test_get_products_view(self):
        response = self.client.get(reverse("shopapp:products_export"))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(products_data["products"], expected_data)


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.credentials = {"username": "testuser", "password": "123456"}
        # cls.user = User.objects.create_user(**cls.credentials)
        cls.user = User.objects.create_user(username="testuser", password="123456")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        # self.client.login(**self.credentials)
        self.client.force_login(self.user)

    def test_order_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_order_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        # self.assertRedirects(response, str(settings.LOGIN_URL))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="testuser", password="123456")
        content_type = ContentType.objects.get_for_model(Order)
        permission = Permission.objects.get(
            codename="view_order",
            content_type=content_type,
        )
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address="Central street, 24",
            promocode="10",
            user=self.user,
        )

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context["order"].pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    fixtures = [
        "user-fixtures.json",
        "product-fixtures.json",
        "order-fixtures.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="testuser", password="123456", is_staff=True
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_order_list(self):
        response = self.client.get(reverse("shopapp:orders_export"))
        self.assertEqual(response.status_code, 200)

        orders = Order.objects.all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.pk,
                "products": [product.pk for product in order.products.all()],
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(orders_data["orders"], expected_data)
