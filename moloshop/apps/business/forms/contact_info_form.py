
# apps/business/forms/contact_info_form.py


from django import forms
from django.forms import inlineformset_factory

from apps.business.models.business import ContactInfo

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ["location", "address", "order"]
        labels = {
            "location": "Локация",
            "address": "Адрес",
            "order": "Порядок",
        }
        widgets = {
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Локация"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Адрес"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }

