
# apps/users/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from apps.users.models.profile import UserProfile

'''
    Распределяйте контроль доступа через шаблоны и представления,
    где можно показать разные UI или блокировать функционал согласно статусу.
    Middleware используйте только для жёсткой блокировки важных спецстраниц.
    Пусть гости пользуются сайтом, но с ограничениями по форме/функциям.
'''

class EmailVerifiedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Пример: блокируем доступ только к страницам /admin/ или /payments/
        blocked_paths = ["/admin/", "/payments/"]

        if user.is_authenticated and user.profile.user_status == UserProfile.UserStatus.GUEST:
            if any(request.path.startswith(p) for p in blocked_paths):
                return redirect('users:verify_email')

        response = self.get_response(request)
        return response


