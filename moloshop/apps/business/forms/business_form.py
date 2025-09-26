
# apps/business/forms/business_form.py

from django import forms
from apps.business.models.business import Business

class BusinessForm(forms.ModelForm):
    """
    Универсальная форма создания/редактирования бизнесов.
    Поддерживает загрузку логотипа и чекбокс 'очистить'.
    """
    logo_clear = forms.BooleanField(
        required=False,
        label="Очистить логотип",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Business
        fields = ["title", "description", "logo", "is_visible"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_visible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Если пользователь отметил очистку логотипа, удаляем его
        if self.cleaned_data.get("logo_clear") and instance.logo:
            instance.logo.delete(save=False)
            instance.logo = None

        if commit:
            instance.save()
        return instance
