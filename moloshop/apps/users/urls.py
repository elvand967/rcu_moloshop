
# apps/users/urls.py

from django.urls import path
from .views.log import *
from .views.profiles import UserProfileEditView, UploadAvatarView, ResetAvatarView
from .views.register import register_view
from .views.verify_email import verify_email_view, resend_email_code_view
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('verify-email/', verify_email_view, name='verify_email'),
    path('verify-email/resend/', resend_email_code_view, name='resend_email_code'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url='/users/password_change_done/'
    ), name='password_change'),

    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    ), name='password_change_done'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("profile/edit/", UserProfileEditView.as_view(), name="profile_edit"),
    path("profile/upload-avatar/", UploadAvatarView.as_view(), name="upload_avatar"),
    path("profile/reset-avatar/", ResetAvatarView.as_view(), name="reset_avatar"),

    # Форма запроса на сброс пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.txt',
        html_email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        success_url='/users/password_reset_done/'
    ), name='password_reset'),

    # Страница уведомления об отправке письма
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    # Страница для установки нового пароля (ссылка из письма)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url='/users/reset/done/'
    ), name='password_reset_confirm'),

    # Страница успешной смены пароля после сброса
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]
