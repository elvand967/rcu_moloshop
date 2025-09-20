
# ../apps/users/models/menu.py

from django.core.exceptions import ValidationError
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from apps.core.models import UUIDModel


class ProfileMenuCategory(UUIDModel, MPTTModel):
    """
    Древовидная модель меню личного кабинета.
    Хранит имя пункта меню, путь (url_name), slug и параметры для reverse().
    """
    name = models.CharField(max_length=100)
    url = models.CharField(
        max_length=200,
        blank=True,
        help_text="Имя URL-шаблона с namespace (например: 'landing:policy_detail')"
    )
    url_params = models.JSONField(
        blank=True,
        null=True,
        help_text='Параметры для reverse(), например: {"slug":"politika-konfidentsialnosti"}'
    )
    # внешний путь
    external_url = models.URLField(
        blank=True,
        null=True,
        help_text="Внешняя ссылка (например: https://t.me/moloshop)"
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.PositiveIntegerField(default=0)
    is_active_link = models.BooleanField(default=True, help_text="Активная ссылка")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class MPTTMeta:
        order_insertion_by = ['order']


    class Meta:
        app_label = 'users'
        verbose_name = "Пункт меню"
        verbose_name_plural = "Меню личного кабинета"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        if self.url:
            try:
                if self.url_params:
                    return reverse(self.url, kwargs=self.url_params)
                return reverse(self.url)
            except:
                return '#'
        return self.url

    def clean(self):
        if self.url and self.external_url:
            raise ValidationError("Нельзя одновременно задать Django-URL и внешнюю ссылку.")
        if not self.url and not self.external_url:
            raise ValidationError("Нужно указать либо Django-URL, либо внешнюю ссылку.")
