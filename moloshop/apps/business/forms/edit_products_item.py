
# apps/business/forms/edit_products_item.py

from django import forms

def get_item_form(model_class):
    """
    Возвращает готовую ModelForm для модели model_class (Goods или Service)
    """
    class ItemForm(forms.ModelForm):
        class Meta:
            model = model_class
            fields = ["title", "image", "description", "price", "is_active"]
            widgets = {
                "title": forms.TextInput(attrs={"class": "form-control"}),
                "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
                "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
                "price": forms.NumberInput(attrs={"class": "form-control"}),
                "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Если модели нет поля image — удаляем поле
            if not hasattr(model_class, "image"):
                self.fields.pop("image", None)

    return ItemForm
