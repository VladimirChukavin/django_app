from timeit import default_timer
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
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
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from shopapp.models import Product, Order, ProductImage
from .forms import ProductForm, OrderForm
from .serializers import ProductSerializer, OrderSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    search_fields = [
        "name",
        "description",
    ]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related("user").prefetch_related("products")
    serializer_class = OrderSerializer
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = [
        "delivery_address",
        "products",
    ]
    ordering_fields = [
        "created_at",
    ]


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


class ProductCreateView(CreateView):
    model = Product
    # fields = ("name", "price", "description", "discount")
    form_class = ProductForm
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    # fields = ("name", "price", "description", "discount", "preview")
    form_class = ProductForm
    template_name_suffix = "_update_form"

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
                "user": order.user.pk,
                "products": [product.pk for product in order.products.all()],
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})
