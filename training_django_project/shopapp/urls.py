from django.urls import path

from shopapp import views

app_name = "shopapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.get_products_list, name="products_list"),
    path("products/create/", views.create_product, name="create_product"),
    path("orders/", views.get_orders_list, name="orders_list"),
    path("orders/create/", views.create_order, name="crate_order"),
]
