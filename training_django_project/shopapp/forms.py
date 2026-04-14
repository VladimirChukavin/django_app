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


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "price", "description", "discount")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("delivery_address", "promocode", "user", "products")
