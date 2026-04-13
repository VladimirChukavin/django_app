from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def process_get_view(request: HttpRequest) -> HttpResponse:
    one = request.GET.get("one", "")
    two = request.GET.get("two", "")
    result = one + two
    context = {
        "one": one,
        "two": two,
        "result": result,
    }

    return render(request, "requestdataapp/request-query-params.html", context=context)


def process_user_form(request: HttpRequest) -> HttpResponse:
    return render(request, "requestdataapp/user-bio-form.html")


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    max_file_size = 1024 * 1024
    message = ""

    if request.method == "POST" and request.FILES.get("myfile"):
        file = request.FILES["myfile"]
        if file.size > max_file_size:
            message = "Ошибка: файл больше допустимого размера 1 МБ"
        else:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            message = f"Файл {filename} успешно загружен"

    context = {
        "message": message,
    }

    return render(request, "requestdataapp/file-upload.html", context=context)
