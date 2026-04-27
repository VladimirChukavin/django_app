from django.urls import path

from myapiapp import views
from .views import GroupListView

app_name = "myapiapp"

urlpatterns = [
    path("hello-world/", views.hello_world_view, name="hello_world"),
    path("groups/", GroupListView.as_view(), name="groups"),
]
