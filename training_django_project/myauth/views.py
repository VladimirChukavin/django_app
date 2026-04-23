from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView

from .models import Profile


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about_me")

    def form_valid(self, form):
        response = super().form_valid(form=form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)

        return response


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/admin/")

        return render(request, "myauth/login.html")

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("/admin/")

    return render(request, "myauth/login.html", {"error": "Invalid login credentials"})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("myauth:login"))


class MyLogoutView(LogoutView):
    http_method_names = ["get", "post", "head", "options", "delete", "put"]
    next_page = reverse_lazy("myauth:login")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie Set")
    response.set_cookie("one", "time", max_age=3600)
    return response


def get_cookies_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("one", "default_value")
    return HttpResponse(f"Value of cookie one : {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["spice"] = "must_flow"
    return HttpResponse("Session set")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("spice", "default_value")
    return HttpResponse(f"Session value: {value!r}")
