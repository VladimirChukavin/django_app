from django import forms
from django.core import validators

from .models import Product, Order


# class ProductForm(forms.Form):
#     name = forms.CharField(label="Name", max_length=100)
#     price = forms.DecimalField(
#         label="Price", max_digits=8, decimal_places=2, min_value=1, max_value=10000000
#     )
#     description = forms.CharField(
#         label="Description",
#         widget=forms.Textarea(attrs={"rows": 3, "cols": 50}),
#         validators=[
#             validators.RegexValidator(
#                 regex=r"great",
#                 message="Field must contain the word 'great'",
#             )
#         ],
#     )
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "price", "description", "discount", "preview")

    image = MultipleFileField()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("delivery_address", "promocode", "user", "products")
