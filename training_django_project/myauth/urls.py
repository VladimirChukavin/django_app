from django.contrib.auth.views import LoginView
from django.urls import path

from myauth import views
from .views import (
    MyLogoutView,
    AboutMeView,
    RegisterView,
    UsersListView,
    UserDetailView,
    UserUpdateProfileView,
    HelloView,
)

app_name = "myauth"

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    # path("login/", views.login_view, name="login"),
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about_me"),
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UsersListView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/update/", UserUpdateProfileView.as_view(), name="user_update"),
    # path("logout/", views.logout_view, name="logout"),
    path("cookie/get/", views.get_cookies_view, name="get_cookies"),
    path("cookie/set/", views.set_cookie_view, name="set_cookies"),
    path("session/get/", views.get_session_view, name="get_session"),
    path("session/set/", views.set_session_view, name="set_session"),
]
