from timeit import default_timer
from datetime import datetime

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    products = [("Laptop", 40000), ("Desktop", 60000), ("Smartphone", 100000)]
    context = {
        "time_running": default_timer(),
        "products": products,
        "date": datetime.now(),
    }

    return render(request, "shopapp/shop-index.html", context=context)
