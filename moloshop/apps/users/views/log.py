# apps/users/log.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib import messages
from apps.users.models.custom_user import CustomUser
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


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
