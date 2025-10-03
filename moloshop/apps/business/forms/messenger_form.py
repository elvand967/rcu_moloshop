
# apps/business/forms/messenger_form.py

from django.forms import inlineformset_factory
from apps.business.models.business import ContactInfo, Messenger
from django import forms

class MessengerForm(forms.ModelForm):
    class Meta:
        model = Messenger
        fields = ["messenger_type", "identifier"]
        labels = {
            "messenger_type": "Тип мессенджера",
            "identifier": "Идентификатор или ссылка",
        }
        widgets = {
            "messenger_type": forms.Select(attrs={"class": "form-select"}),
            "identifier": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите идентификатор"}),
        }

MessengerFormSet = inlineformset_factory(
    ContactInfo, Messenger,
    form=MessengerForm,
    extra=1,  # новая строка мессенджера
    can_delete=True
)

