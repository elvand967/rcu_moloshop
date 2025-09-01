
# apps/users/forms/user_profile_form.py

from django import forms
from django.contrib.auth import get_user_model
from apps.users.models import UserProfile


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

class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,  # если поле не обязательное
        label='День рождения',  # задаем нужную метку
        input_formats=['%d/%m/%Y'],  # формат ввода: День(2)/Месяц(2)/Год(4)
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'placeholder': 'ДД/ММ/ГГГГ',
                'class': 'form-control',
                'type': 'date'  # можно задать календарь, но формат в браузерах разный
            }
        )
    )

    class Meta:
        model = UserProfile
        fields = [
            'phone_number_display', 'date_of_birth', 'bio',
            'website', 'location', 'gender'
        ]

class AvatarForm(forms.Form):
    avatar_file = forms.ImageField(required=True)

