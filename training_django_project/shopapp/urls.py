from django.urls import path

from shopapp import views
from .views import (
    IndexView,
    ProductsListView,
    ProductCreateView,
    ProductDetailsView,
    OrdersListView,
    OrderDetailsView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDataExportView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    OrdersExportView,
)

app_name = "shopapp"

urlpatterns = [
    # path("", views.index, name="index"),
    # path("products/", views.get_products_list, name="products_list"),
    # path("products/create/", views.create_product, name="create_product"),
    # path("orders/", views.get_orders_list, name="orders_list"),
    # path("orders/create/", views.create_order, name="create_order"),
    path("", IndexView.as_view(), name="index"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/export/", ProductDataExportView.as_view(), name="products_export"),
    path("products/create/", ProductCreateView.as_view(), name="create_product"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path(
        "products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/export/", OrdersExportView.as_view(), name="orders_export"),
    path("orders/create/", OrderCreateView.as_view(), name="create_order"),
    path("orders/<int:pk>", OrderDetailsView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
]
