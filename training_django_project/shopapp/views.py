from timeit import default_timer
from datetime import datetime

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse

from shopapp.models import Product, Order
from .forms import ProductForm, OrderForm


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


def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            # price = form.cleaned_data["price"]
            # Product.objects.create(name=name, price=price)
            # Product.objects.create(**form.cleaned_data)
            form.save()
            url = reverse("shopapp:products_list")
            return redirect(url)
    else:
        form = ProductForm()

    context = {
        "form": form,
    }
    return render(request, "shopapp/create-product.html", context=context)


def get_orders_list(request: HttpRequest) -> HttpResponse:
    context = {
        "orders": Order.objects.select_related("user")
        .prefetch_related("products")
        .all(),
    }
    return render(request, "shopapp/orders-list.html", context=context)


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            form.save()
            url = reverse("shopapp:orders_list")
            return redirect(url)
    else:
        form = OrderForm()

    context = {
        "form": form,
    }
    return render(request, "shopapp/create-order.html", context=context)
