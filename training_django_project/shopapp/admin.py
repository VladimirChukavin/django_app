from csv import DictReader
from io import TextIOWrapper

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .common import save_csv_products
from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm


class OrderInline(admin.TabularInline):
    model = Product.orders.through


class ProductImageInLine(admin.StackedInline):
    model = ProductImage


@admin.action(description="Archieved products")
def mark_archived(
    modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet
):
    queryset.update(archived=True)


@admin.action(description="Unarchieved products")
def mark_unarchived(
    modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet
):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = "shopapp/products_changelist.html"
    actions = (
        mark_archived,
        mark_unarchived,
        "export_as_csv",
    )
    inlines = (
        OrderInline,
        ProductImageInLine,
    )
    list_display = ("pk", "name", "description_short", "price", "discount", "archived")
    list_display_links = ("pk", "name")
    ordering = ("pk", "name")
    search_fields = ("name", "description", "price")
    fieldsets = [
        (None, {"fields": ("name", "description")}),
        (
            "Price and discount info:",
            {
                "fields": ("price", "discount"),
                "classes": ("collapse", "wide"),
            },
        ),
        (
            "Images:",
            {
                "fields": ("preview",),
            },
        ),
        (
            "Extra options",
            {
                "fields": ("archived",),
                "classes": ("collapse",),
                "description": "If archived is checked - product will not be shown on the site",
            },
        ),
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 56:
            return obj.description
        return obj.description[:56] + "..."

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context=context)

        form = CSVImportForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context=context, status=400)

        # csv_file = TextIOWrapper(
        #     form.files['csv_file'].file,
        #     encoding=request.encoding,
        # )
        # reader = DictReader(csv_file)
        # products = [Product(**row) for row in reader]
        # Product.objects.bulk_create(products)
        save_csv_products(
            file=form.files["csv_file"].file,
            encoding=request.encoding,
        )
        self.message_user(request, "Products imported successfully")

        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("import-products-csv/", self.import_csv, name="import_products_csv"),
        ]
        return new_urls + urls


# admin.site.register(Product, ProductAdmin)


class ProductInline(admin.TabularInline):
    # class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders_changelist.html"
    inlines = [ProductInline]
    list_display = ("pk", "delivery_address", "promocode", "created_at", "user_verbose")
    list_display_links = ("pk", "delivery_address")

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context=context)

        form = CSVImportForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context=context, status=400)

        csv_file = TextIOWrapper(
            form.files["csv_file"].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)

        orders_to_create = []
        orders_products_to_add = []

        for row in reader:
            try:
                user_id = int(row["user"])
                user = User.objects.get(pk=user_id)
            except (User.DoesNotExist, ValueError):
                self.message_user(request, f'Invalid user ID: {row["user"]}')

            order = Order(
                delivery_address=row["delivery_address"],
                promocode=row["promocode"],
                user=user,
            )
            orders_to_create.append(order)

            products_ids_str = row.get("products", "")
            if products_ids_str.strip():
                try:
                    products_ids = [
                        int(pid.strip()) for pid in products_ids_str.split(",")
                    ]
                except ValueError as e:
                    self.message_user(request, f"Invalid product ID: {e}")

                for pid in products_ids:
                    orders_products_to_add.append((order, pid))

        with transaction.atomic():
            Order.objects.bulk_create(orders_to_create)

            products_in_order = []
            for order, product_id in orders_products_to_add:
                try:
                    product = Product.objects.get(pk=product_id)
                    products_in_order.append(
                        Order.products.through(order=order, product=product)
                    )
                except Product.DoesNotExist:
                    self.message_user(request, f"Product #{product_id} does not exist")

            Order.products.through.objects.bulk_create(products_in_order)

        self.message_user(request, "Orders imported successfully")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("import-orders-csv/", self.import_csv, name="import_orders_csv"),
        ]
        return new_urls + urls
