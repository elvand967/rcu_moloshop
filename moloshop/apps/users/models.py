
# ../apps/users/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from ..core.models import UUIDModel


class CustomUser(UUIDModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='Фамилия')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # можно добавить, например, first_name

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'
