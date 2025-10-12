
# apps/business/forms/productss_form.py


from django import forms
from datetime import timedelta
from apps.business.models.business_products import Goods, Service


class GoodsTitleForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ["title",]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Название товара"
            }),
        }


class GoodsForm(forms.ModelForm):  # переименовано для соответствия
    class Meta:
        model = Goods  # здесь модель Goods
        fields = ["title", "description", "unit", "price", "currency", "sku", "stock", "delivery_info"]
        labels = {
            "title": "Название товара",
            "unit": "Единица измерения",
            "currency": "Валюта платежа",
            "stock": "В наличии",
            "delivery_info": "Доставка",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название вашего товара ..."}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Опишите ваш товар..."}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "unit": forms.Select(attrs={"class": "form-select"}),
            "currency": forms.Select(attrs={"class": "form-select"}),
            "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "Если есть введите артикул товара..."}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "delivery_info": forms.TextInput(attrs={"class": "form-control", "placeholder": "Укажите 'Самовывоз' или другой способ..."}),
        }


class ServiceTitleForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Название услуги"
            }),
        }


class ServiceForm(forms.ModelForm):
    duration_hhmm = forms.CharField(
        label="Длительность (чч:мм)",
        required=False,
        widget=forms.TimeInput(format="%H:%M", attrs={
            "type": "time",
            "class": "form-control col-8 col-sm-12",
        }),
    )

    class Meta:
        model = Service
        fields = ["title", "description", "unit", "price", "currency",
                  "duration_hhmm", "place_of_service", "staff", "sku", "is_active"]

        widgets = {
                "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # при редактировании существующей услуги заполняем duration_hhmm
        if self.instance and self.instance.duration:
            total_seconds = int(self.instance.duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            self.fields["duration_hhmm"].initial = f"{hours:02d}:{minutes:02d}"

    def clean_duration_hhmm(self):
        """Преобразуем ввод 'HH:MM' в timedelta"""
        value = self.cleaned_data.get("duration_hhmm")
        if not value:
            return None
        try:
            hours, minutes = map(int, value.split(":"))
            return timedelta(hours=hours, minutes=minutes)
        except Exception:
            raise forms.ValidationError("Введите длительность в формате ЧЧ:ММ")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.duration = self.cleaned_data.get("duration_hhmm")
        if commit:
            instance.save()
        return instance
