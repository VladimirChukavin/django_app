from django.urls import path

from shopapp import views

app_name = "shopapp"

urlpatterns = [
    path("", views.index, name="index"),
]
