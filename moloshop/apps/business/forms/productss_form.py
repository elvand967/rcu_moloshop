
# apps/business/forms/productss_form.py

from django import forms
from apps.business.models.business_products import Product, Service


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "unit", "price", "currency", "sku", "stock", "delivery_info"]
        # Переопределим/назначим label
        labels = {
            "title": "Название товара",
            "unit": "Единица измерения",
            "currency": "Валюта платежа",
            "stock": "В наличии",
            "delivery_info": "Доставка",
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Название вашего товара ...",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control", "rows": 3,
                "placeholder": "Опишите ваш товар...",
            }),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "unit": forms.Select(attrs={"class": "form-select"}),
            "currency": forms.Select(attrs={"class": "form-select"}),
            "sku": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Если есть введите артикул товара...",
            }),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "delivery_info": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Укажите 'Самовывоз' или другой способ...",
            }),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["title", "description", "unit", "price", "currency", "duration", "place_of_service", "staff", "sku"]
        labels = {
            "title": "Название услуги",
            "unit": "Единица измерения",
            "currency": "Валюта платежа",
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Название вашей услуги ...",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control", "rows": 3,
                "placeholder": "Опишите вашу услугу...",
            }),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "unit": forms.Select(attrs={"class": "form-select"}),
            "currency": forms.Select(attrs={"class": "form-select"}),
            "duration": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: 01:30:00"}),
            "place_of_service": forms.TextInput(attrs={"class": "form-control"}),
            "staff": forms.Select(attrs={"class": "form-select"}),
            "sku": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Если есть введите артикул услуги...",
            }),
        }
