
# ../apps/users/models/menu.py

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from apps.core.models import UUIDModel

class ProfileMenuCategory(UUIDModel, MPTTModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile_menu_categories",
        verbose_name="Пользователь",
        null=True,
        blank=True,
        help_text="Пользователь для персональных пунктов меню. Пусто — для общего меню."
    )
    name = models.CharField(max_length=100, verbose_name="Название пункта меню")
    url = models.CharField(max_length=200, blank=True, verbose_name="Имя URL-шаблона",
                           help_text="Имя URL-шаблона с namespace (например: 'landing:policy_detail')")
    url_params = models.JSONField(blank=True, null=True, verbose_name="Параметры для URL",
                                 help_text='Параметры для reverse(), например: {"slug":"politika-konfidentsialnosti"}')
    external_url = models.URLField(blank=True, null=True, verbose_name="Внешняя ссылка",
                                   help_text="Внешняя ссылка (например: https://t.me/moloshop)")
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                           related_name="children", verbose_name="Родительский пункт меню")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active_link = models.BooleanField(default=True, verbose_name="Активная ссылка",
                                         help_text="Если выключена, пункт меню не активен")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class MPTTMeta:
        order_insertion_by = ["order"]

    class Meta:
        app_label = "users"
        verbose_name = "Пункт меню"
        verbose_name_plural = "Меню личного кабинета"
        ordering = ["order"]
        unique_together = ("user", "name", "parent")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        if self.url:
            try:
                if self.url_params:
                    return reverse(self.url, kwargs=self.url_params)
                return reverse(self.url)
            except Exception:
                return "#"
        elif self.external_url:
            return self.external_url
        return "#"

    def clean(self):
        if self.url and self.external_url:
            raise ValidationError("Нельзя одновременно задать Django-URL и внешнюю ссылку.")
        if not self.url and not self.external_url:
            raise ValidationError("Нужно указать либо Django-URL, либо внешнюю ссылку.")

