
# apps/users/views/verify_email.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.users.models import UserProfile


@login_required
def verify_email_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        input_code = request.POST.get('email_code', '').strip()

        if (profile.email_code == input_code) and profile.is_email_code_valid():
            profile.user_status = UserProfile.UserStatus.USER
            profile.email_code = ''
            profile.email_code_created = None
            profile.save()
            messages.success(request, 'Email успешно подтвержден! Регистрация завершена.')
            return redirect('users:profile_edit')
        else:
            messages.error(request, 'Неверный или просроченный код. Попробуйте снова.')

    return render(request, 'users/verify_email.html', {'email': user.email})


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from apps.users.utils.email_utils import send_email_confirmation_code

@login_required
def resend_email_code_view(request):
    user = request.user
    send_email_confirmation_code(user)  # сгенерирует новый код и отправит письмо
    messages.success(request, 'Новый код подтверждения отправлен на ваш email.')
    return redirect('users:verify_email')
