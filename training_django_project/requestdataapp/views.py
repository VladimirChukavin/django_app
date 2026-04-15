from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import UserBioForm, UploadFileForm


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
    context = {
        "form": UserBioForm(),
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    max_file_size = 1024 * 1024
    message = ""

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            # file = request.FILES["myfile"]
            file = form.cleaned_data["file"]
            if file.size > max_file_size:
                message = "Ошибка: файл больше допустимого размера 1 МБ"
            else:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                message = f"Файл {filename} успешно загружен"
    else:
        form = UploadFileForm()

    context = {
        "form": form,
        "message": message,
    }

    return render(request, "requestdataapp/file-upload.html", context=context)
