
# apps/users/views/register.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from apps.users.models import UserProfile
from apps.users.models.custom_user import CustomUser
from apps.users.utils.email_utils import send_email_confirmation_code

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not email or not password or not password2:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
            return render(request, 'users/register.html')

        if password != password2:
            messages.error(request, 'Пароли не совпадают.')
            return render(request, 'users/register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже зарегистрирован.')
            return render(request, 'users/register.html')

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True  # пользователь сразу активен
        )
        # Устанавливаем статус Гость (0) в профиле
        user.profile.user_status = UserProfile.UserStatus.GUEST  # правильное обращение к константе
        user.profile.save()

        login(request, user)
        send_email_confirmation_code(user)
        return redirect('users:verify_email')

    return render(request, 'users/register.html')
