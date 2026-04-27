"""
В этом модуле описаны представления для приложения shopаpp.

Разные представления для товаров, заказов и пользователей.
"""

from timeit import default_timer
from datetime import datetime

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from shopapp.models import Product, Order, ProductImage
from .forms import ProductForm, OrderForm


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
            "items": 0,
            "date": datetime.now(),
        }

        return render(request, "shopapp/shop-index.html", context=context)


class ProductsListView(ListView):
    template_name = "shopapp/products_list.html"
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = "products"


class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        # return self.request.user.is_superuser
        return self.request.user.has_perm("shopapp.add_product")

    model = Product
    # fields = ("name", "price", "description", "discount")
    form_class = ProductForm
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form=form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    # fields = ("name", "price", "description", "discount", "preview")
    form_class = ProductForm
    template_name_suffix = "_update_form"

    def test_func(self):
        product = self.get_object()

        if self.request.user.is_superuser:
            return True

        return (
            self.request.user.has_perm("shopapp.change_product")
            and product.created_by == self.request.user
        )

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        files = form.cleaned_data["image"]
        for image in files:
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )

        return response


class ProductDetailsView(DetailView):
    template_name = "shopapp/product_details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
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


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = ["shopapp.view_order"]
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
                "user": order.user.pk,
                "products": [product.pk for product in order.products.all()],
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})
