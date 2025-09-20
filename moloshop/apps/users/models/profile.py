
# apps/users/models/profile.py

from django.utils.translation import gettext_lazy as _
from datetime import timedelta
import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.core.models import UUIDModel
from apps.users.utils.avatar import (
    generate_avatar_image,
    process_uploaded_avatar,
    delete_old_avatar,
    avatar_upload_to
)

class UserProfile(UUIDModel):
    class UserStatus(models.IntegerChoices):
        GUEST = 0, _("Гость")
        USER = 1, _("Пользователь")
        EMPLOYEE = 2, _("Сотрудник")
        MASTER = 3, _("Мастер")
        MANAGER = 4, _("Руководитель")
        ADMIN = 5, _("Администратор")
        SUPERUSER = 6, _("Суперпользователь")

    user_status = models.PositiveSmallIntegerField(
        choices=UserStatus.choices,
        default=UserStatus.GUEST,
        verbose_name=_("Статус пользователя")
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("Пользователь")
    )
    avatar = models.ImageField(
        _("Аватар"),
        upload_to=avatar_upload_to,
        blank=True,
        null=True,
    )
    phone_number_display = models.CharField(
        _("Телефон"),
        max_length=50,
        blank=True,
        help_text=_("Формат на усмотрение пользователя: +375(25)963-3344 или 103"),
    )
    phone_number_digits = models.CharField(
        _("Телефон (только цифры)"),
        max_length=50,
        blank=True,
        help_text=_("Автоматически генерируется из поля 'Телефон (как ввёл пользователь)'"),
    )
    date_of_birth = models.DateField(verbose_name=_("Дата рождения"), null=True, blank=True)
    bio = models.TextField(blank=True, null=True, max_length=500, verbose_name=_('О себе'))
    website = models.URLField(blank=True, null=True, verbose_name=_('Веб-сайт'))
    location = models.CharField(_("Локация"), max_length=255, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=(('male', _('Мужской')), ('female', _('Женский')), ('other', _('Другое'))),
        blank=True, null=True, verbose_name=_('Пол')
    )
    is_active_user = models.BooleanField(default=True, help_text=_('Активный пользователь'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создан"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлен"))
    email_code = models.CharField(max_length=6, blank=True, null=True, verbose_name=_("Код подтверждения email"))
    email_code_created = models.DateTimeField(blank=True, null=True, verbose_name=_("Время создания кода"))

    def save(self, *args, **kwargs):
        # обработка телефона
        if self.phone_number_display:
            self.phone_number_digits = "".join(ch for ch in self.phone_number_display if ch.isdigit())
        else:
            self.phone_number_digits = ""

        super().save(*args, **kwargs)

    def upload_avatar(self, file):
        """Загрузить новую аватарку"""
        if self.avatar:
            delete_old_avatar(self.avatar.name)
        processed = process_uploaded_avatar(file, user=self.user)
        self.avatar.save(processed.name, processed, save=True)

    def reset_avatar(self):
        """Сбросить на дефолтную аватарку"""
        delete_old_avatar(self.avatar.path if self.avatar else None)
        default_avatar = generate_avatar_image(self.user)
        self.avatar.save(default_avatar.name, default_avatar, save=True)

    def is_email_code_valid(self, timeout_minutes=10):
        if not self.email_code_created:
            return False
        return timezone.now() < self.email_code_created + timedelta(minutes=timeout_minutes)

    def __str__(self):
        return f"Профиль {self.user.email}"

    class Meta:
        verbose_name = _("Профиль пользователя")
        verbose_name_plural = _("Профили пользователей")
