
# apps/users/urls.py

from django.urls import path, reverse_lazy
from .views.log import *
from .views.profiles import UserProfileEditView, UploadAvatarView, ResetAvatarView
from .views.register import register_view
from .views.verify_email import verify_email_view, resend_email_code_view
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    # Вход в систему
    path('login/', login_view, name='login'),

    # Выход из системы
    path('logout/', logout_view, name='logout'),

    # Регистрация нового пользователя
    path('register/', register_view, name='register'),

    # Подтверждение email и повторная отправка кода
    path('verify-email/', verify_email_view, name='verify_email'),
    path('verify-email/resend/', resend_email_code_view, name='resend_email_code'),

    # Смена пароля - форма смены пароля и редирект после успеха
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='users/components/password_change.html',
        success_url=reverse_lazy('users:password_change_done')
    ), name='password_change'),

    # Уведомление об успешной смене пароля
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/components/password_change_done.html'
    ), name='password_change_done'),

    # Профиль и связанные действия (редактирование, аватар)
    path('profile/', ProfileView.as_view(), name='profile'),
    path("profile/edit/", UserProfileEditView.as_view(), name="profile_edit"),
    path("profile/upload-avatar/", UploadAvatarView.as_view(), name="upload_avatar"),
    path("profile/reset-avatar/", ResetAvatarView.as_view(), name="reset_avatar"),

    # Запрос сброса пароля (ввод email), редирект после отправки письма
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/components/password_reset.html',
        email_template_name='users/components/password_reset_email.txt',
        html_email_template_name='users/components/password_reset_email.html',
        subject_template_name='users/components/password_reset_subject.txt',
        success_url=reverse_lazy('users:password_reset_done')
    ), name='password_reset'),

    # Уведомление об отправке письма для сброса пароля
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/components/password_reset_done.html'
    ), name='password_reset_done'),

    # Подтверждение сброса (установка нового пароля в ссылке из письма),
    # редирект на страницу успешного сброса
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/components/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),

    # Страница успешного завершения сброса пароля
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/components/password_reset_complete.html'
    ), name='password_reset_complete'),
]

