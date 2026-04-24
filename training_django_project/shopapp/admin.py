from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin


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


# admin.site.register(Product, ProductAdmin)


class ProductInline(admin.TabularInline):
    # class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ("pk", "delivery_address", "promocode", "created_at", "user_verbose")
    list_display_links = ("pk", "delivery_address")

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
