# apps/users/log.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib import messages
from apps.users.models.custom_user import CustomUser
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # Проверка заполненности
        if not email or not password or not password2:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
            return render(request, 'users/register.html')

        # Проверка совпадения паролей
        if password != password2:
            messages.error(request, 'Пароли не совпадают.')
            return render(request, 'users/register.html')

        # Email занят?
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже зарегистрирован.')
            return render(request, 'users/register.html')

        # Можно добавить дополнительные правила (длина пароля, проверка сложности и пр.)

        # Создание пользователя
        user = CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно!')
        return redirect('users:profile_edit')

    return render(request, 'users/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:profile_edit')
        else:
            messages.error(request, 'Неверный e-mail или пароль.')

    return render(request, 'users/login.html')


def logout_view(request):
    auth_logout(request)
    return render(request, 'users/logout.html')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
