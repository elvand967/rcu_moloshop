
# apps/users/forms/user_profile_form.py

from apps.users.models import UserProfile
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        help_texts = {
            'email': 'Ваш email — ваш логин, изменить нельзя',
            'first_name': 'Введите ваше имя',
            'last_name': 'Введите вашу фамилию',
        }

        # Запретим редактирование в форме Профиль - Email
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        email_readonly = kwargs.pop('email_readonly', False)
        email_error = kwargs.pop('email_error', False)
        super().__init__(*args, **kwargs)
        if email_readonly:
            self.fields['email'].widget.attrs['readonly'] = True
            # Убираем класс ошибки, если был
            self.fields['email'].widget.attrs.pop('class', None)
        if email_error:
            classes = self.fields['email'].widget.attrs.get('class', '')
            classes += ' email-error'
            self.fields['email'].widget.attrs['class'] = classes.strip()


class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        label=_('День рождения'),
        input_formats=['%Y-%m-%d'],  # разрешаем только ISO-формат
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control',
                'type': 'date',               # браузер сам подскажет формат
                'placeholder': 'ГГГГ-ММ-ДД',  # явный ISO placeholder
            }
        )
    )

    class Meta:
        model = UserProfile
        fields = [
            'phone_number_display', 'date_of_birth', 'bio',
            'website', 'location', 'gender'
        ]
        widgets = {
            'phone_number_display': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }


class AvatarForm(forms.Form):
    avatar_file = forms.ImageField(required=True)

