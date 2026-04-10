from timeit import default_timer
from datetime import datetime

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from shopapp.models import Product, Order


def index(request: HttpRequest) -> HttpResponse:
    products = [("Laptop", 40000), ("Desktop", 60000), ("Smartphone", 100000)]
    context = {
        "time_running": default_timer(),
        "products": products,
        "date": datetime.now(),
    }

    return render(request, "shopapp/shop-index.html", context=context)


def get_products_list(request: HttpRequest) -> HttpResponse:
    context = {
        "products": Product.objects.all(),
    }
    return render(request, "shopapp/products-list.html", context=context)


def get_orders_list(request: HttpRequest) -> HttpResponse:
    context = {
        "orders": Order.objects.select_related("user")
        .prefetch_related("products")
        .all(),
    }
    return render(request, "shopapp/orders-list.html", context=context)
