from random import random

from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    DetailView,
)
from django.utils.translation import gettext_lazy as _, ngettext
from django.views.decorators.cache import cache_page

from .forms import ProfileAvatarForm
from .models import Profile


class HelloView(View):
    welcome_message = _("welcome hello world")

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items", 0)
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(f"<h1>{self.welcome_message}</h1><h2>{products_line}</h2>")


class AboutMeView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "myauth/about-me.html"
    form_class = ProfileAvatarForm
    success_url = reverse_lazy("myauth:about_me")

    def get_object(self) -> Profile:
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_object()
        return context


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


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "myauth/users_list.html"
    context_object_name = "users"
    queryset = User.objects.select_related("profile").all()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "myauth/user_detail.html"
    context_object_name = "user_obj"

    def get_queryset(self):
        return User.objects.select_related("profile")


class UserUpdateProfileView(UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = "myauth/user_update.html"
    form_class = ProfileAvatarForm
    context_object_name = "profile"

    def get_success_url(self):
        return reverse("myauth:user_detail", kwargs={"pk": self.object.user.pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user.is_staff or self.request.user == profile.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_edit"] = self.test_func()
        return context


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


@cache_page(60)
def get_cookies_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("one", "default_value")
    return HttpResponse(f"Value of cookie one : {value!r} + {random()}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["spice"] = "must_flow"
    return HttpResponse("Session set")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("spice", "default_value")
    return HttpResponse(f"Session value: {value!r}")
