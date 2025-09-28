# apps/business/forms/business_form.py

from django import forms
from apps.business.models.business import Business


class BusinessForm(forms.ModelForm):
    """
    Форма редактирования бизнеса: доступ ко всем полям модели.
    """

    class Meta:
        model = Business

        # fields = "__all__"   # теперь на фронт уйдут ВСЕ поля модели
        # Выбор требуемых полей и очередность их отображения:
        fields = ["title", "subtitle", "description", "is_visible"]

        # Переопределим/назначим label
        labels = {
            "title": "Название бизнеса",
            "subtitle": "Подзаголовок",
            "description": "Описание",
            "is_visible": "Активный",
        }

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control form-control--large",
                "placeholder": "Название вашего бизнеса ..."
            }),
            "subtitle": forms.TextInput(attrs={
                "class": "form-control form-control--large",
                "placeholder": "Подзаголовок вашего бизнеса ..."
            }),
            "slug": forms.TextInput(attrs={"class": "form-control"}),  # если slug редактируемый
            "description": forms.Textarea(attrs={
                "class": "form-control form-control--compact",
                "rows": 3,
                "placeholder": "Опишите ваш бизнес..."
            }),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "is_visible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "created_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "updated_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }
        # Файловые поля (logo, favicon, banner и т.п.) Django сам отрендерит <input type="file">

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
