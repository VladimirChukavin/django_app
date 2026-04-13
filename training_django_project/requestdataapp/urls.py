from django.urls import path

from requestdataapp import views

app_name = "requestdataapp"

urlpatterns = [
    path("get/", views.process_get_view, name="get-view"),
    path("bio/", views.process_user_form, name="user-form"),
    path("upload/", views.handle_file_upload, name="upload-file"),
]
