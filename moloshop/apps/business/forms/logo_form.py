
# apps/business/forms/logo_form.py

from django import forms

class BusinessLogoForm(forms.Form):
    """
    Простая форма: принимает только файл логотипа.
    Фавикон генерируется автоматически из того же файла.
    """
    logo = forms.ImageField(
        required=True,
        label="Загрузить логотип",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )