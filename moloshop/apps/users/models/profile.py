
# apps/users/models/profile.py

import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.core.models import UUIDModel
from apps.users.utils.avatar import generate_avatar_image, process_uploaded_avatar
from apps.users.utils.storages import OverwriteStorage


def user_avatar_upload_path(instance, filename):
    """avatars/YYYY/MM/<id>.jpg"""
    if instance.user.date_joined:
        year = instance.user.date_joined.year
        month = f"{instance.user.date_joined.month:02d}"
    else:
        from django.utils import timezone
        now = timezone.now()
        year = now.year
        month = f"{now.month:02d}"
    ext = "jpg"
    return os.path.join("avatars", str(year), str(month), f"{instance.user.id}.{ext}")


class UserProfile(UUIDModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("Пользователь")
    )
    avatar = models.ImageField(
        _("Аватар"),
        upload_to=user_avatar_upload_path,
        blank=True,
        null=True,
        storage=OverwriteStorage()
    )
    middle_name = models.CharField(_("Отчество"), max_length=50, blank=True, null=True)
    phone_number_display = models.CharField(
        _("Телефон (как ввёл пользователь)"),
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
    date_of_birth = models.DateField(_("Дата рождения"), null=True, blank=True)
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

    def save(self, *args, **kwargs):
        # 1. Нормализация телефона
        if self.phone_number_display:
            self.phone_number_digits = "".join(ch for ch in self.phone_number_display if ch.isdigit())
        else:
            self.phone_number_digits = ""

        # 2. Если загружена аватарка пользователем, проверяем PNG с прозрачностью
        if self.avatar:
            self.avatar = process_uploaded_avatar(self.avatar)
        else:
            # 3. Если аватарка не загружена, генерируем автоматическую
            self.avatar = generate_avatar_image(self.user, size=400)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Профиль {self.user.email}"

    class Meta:
        verbose_name = _("Профиль пользователя")
        verbose_name_plural = _("Профили пользователей")
