from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View


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


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie Set")
    response.set_cookie("one", "time", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("one", "default_value")
    return HttpResponse(f"Value of cookie one: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["spice"] = "must_flow"
    return HttpResponse("Session set")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("spice", "default_value")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": 12, "bar": True})
