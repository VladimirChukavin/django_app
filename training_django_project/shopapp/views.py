from timeit import default_timer
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from shopapp.models import Product, Order
from .forms import ProductForm, OrderForm


# ============================= Class-based views =================================
class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ("Laptop", 40000),
            ("Desktop", 60000),
            ("Smartphone", 100000),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "date": datetime.now(),
        }

        return render(request, "shopapp/shop-index.html", context=context)


class ProductsListView(ListView):
    template_name = "shopapp/products_list.html"
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = "products"


class ProductCreateView(CreateView):
    model = Product
    # fields = ("name", "price", "description", "discount")
    form_class = ProductForm
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = ("name", "price", "description", "discount")
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )


class ProductDetailsView(DetailView):
    template_name = "shopapp/product_details.html"
    model = Product
    context_object_name = "product"


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})


class OrdersListView(LoginRequiredMixin, ListView):
    template_name = "shopapp/orders_list.html"
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderDetailsView(DetailView):
    template_name = "shopapp/order_details.html"
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    model = Order
    fields = ("delivery_address", "promocode", "user", "products")
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class OrdersExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user,
                "products": order.products,
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})


# ========================== Function-based views ====================================
# class ProductDetailsView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         # product = Product.objects.get(pk=pk)
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             "product": product,
#         }
#         return render(request, "shopapp/product-details.html", context=context)


# def index(request: HttpRequest) -> HttpResponse:
#     products = [("Laptop", 40000), ("Desktop", 60000), ("Smartphone", 100000)]
#     context = {
#         "time_running": default_timer(),
#         "products": products,
#         "date": datetime.now(),
#     }
#
#     return render(request, "shopapp/shop-index.html", context=context)


# def get_products_list(request: HttpRequest) -> HttpResponse:
#     context = {
#         "products": Product.objects.all(),
#     }
#     return render(request, "shopapp/products-list.html", context=context)


# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             # name = form.cleaned_data['name']
#             # price = form.cleaned_data["price"]
#             # Product.objects.create(name=name, price=price)
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse("shopapp:products_list")
#             return redirect(url)
#     else:
#         form = ProductForm()
#
#     context = {
#         "form": form,
#     }
#     return render(request, "shopapp/create-product.html", context=context)


# def get_orders_list(request: HttpRequest) -> HttpResponse:
#     context = {
#         "orders": Order.objects.select_related("user")
#         .prefetch_related("products")
#         .all(),
#     }
#     return render(request, "shopapp/orders-list.html", context=context)


# def create_order(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             url = reverse("shopapp:orders_list")
#             return redirect(url)
#     else:
#         form = OrderForm()
#
#     context = {
#         "form": form,
#     }
#     return render(request, "shopapp/create-order.html", context=context)
