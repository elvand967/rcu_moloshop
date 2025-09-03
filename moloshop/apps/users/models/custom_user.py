
# apps/users/models/custom_user.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from apps.users.managers import CustomUserManager
from apps.core.models import UUIDModel


class CustomUser(UUIDModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Фамилия')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # Важно: эти методы часто ждут как минимум django-админка и чужие плагины
    def get_full_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.email

    def get_short_name(self):
        return self.first_name or self.last_name or self.email

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'