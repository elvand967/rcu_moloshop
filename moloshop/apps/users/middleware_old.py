
# apps/users/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from apps.users.models.profile import UserProfile

class EmailVerifiedMiddleware:
    """
    Middleware проверяет, авторизован ли пользователь,
    и если да, то проверяет его статус user_status.
    Если статус Гость (не подтверждённый email),
    предотвращает доступ ко всем страницам,
    перенаправляя на страницу подтверждения email.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            profile = getattr(user, 'profile', None)
            if profile and profile.user_status == UserProfile.UserStatus.GUEST:
                allowed_paths = [
                    reverse('users:verify_email'),  # Страница подтверждения email
                    reverse('users:logout'),
                    # Можно добавить публичные пути, которые разрешены гостю
                ]
                path = request.path
                if path not in allowed_paths:
                    return redirect('users:verify_email')

        response = self.get_response(request)
        return response

