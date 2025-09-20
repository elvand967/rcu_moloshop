# apps/core/models/footer_menu.py

from django.db import models
from .abstract import UUIDModel
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import MaxValueValidator
from django.urls import reverse, NoReverseMatch


class FooterMenuCategory(UUIDModel, MPTTModel):
    name = models.CharField(max_length=100, blank=True)
    icon = models.ImageField(upload_to="footer_menu_icons", null=True, blank=True)

    # внутренний путь (имя named url)
    url = models.CharField(
        max_length=200,
        blank=True,
        default="#",
        help_text="Имя URL-шаблона с namespace (например: 'core:policy_detail')"
    )

    url_params = models.JSONField(
        blank=True,
        null=True,
        help_text="Параметры для reverse(), например: {'slug': 'privacy-policy'}"
    )

    # внешний путь
    external_url = models.URLField(
        blank=True,
        null=True,
        help_text="Внешняя ссылка (например: https://t.me/moloshop)"
    )

    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    order = models.PositiveIntegerField(default=0)
    col_desctop = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(12)],
        help_text="Количество колонок в строке (0-12) для desktop"
    )
    col_md = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(12)],
        help_text="Количество колонок в строке (0-12) для mobile"
    )
    is_active_link = models.BooleanField(default=True, help_text="Активная ссылка")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class MPTTMeta:
        order_insertion_by = ["order"]

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Меню footer"

    def __str__(self):
        return self.name or f"MenuItem {self.pk}"

    # --- Вспомогательные методы ---
    def get_col_desktop(self):
        if self.col_desctop:
            return self.col_desctop
        return 4 if self.parent is None and self.order < 4 else 12

    def get_col_md(self):
        return self.col_md or 12

    def get_url(self):
        """Формируем реальную ссылку"""
        if self.external_url:
            return self.external_url

        if not self.url or self.url == "#":
            return "#"

        try:
            return reverse(self.url, kwargs=self.url_params or {})
        except NoReverseMatch:
            return "#"






# from django.db import models
# from .abstract import UUIDModel
# from mptt.models import MPTTModel, TreeForeignKey
# from django.core.validators import MaxValueValidator
# from django.urls import reverse, NoReverseMatch
#
#
# class FooterMenuCategory(UUIDModel, MPTTModel):
#     name = models.CharField(max_length=100)
#     icon = models.ImageField(upload_to='footer_menu_icons', null=True, blank=True)
#     url = models.CharField(
#         max_length=200,
#         blank=True,
#         default="#",
#         help_text="Имя URL-шаблона с namespace (например: 'core:policy_detail')"
#     )
#     url_params = models.JSONField(
#         blank=True,
#         null=True,
#         help_text="Параметры для reverse(), например: {'slug': 'privacy-policy'}"
#     )
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
#     order = models.PositiveIntegerField(default=0)
#     col_desctop = models.PositiveIntegerField(
#         default=0,
#         validators=[MaxValueValidator(12)],
#         help_text="Количество колонок в строке (0-12) для desktop"
#     )
#     col_md = models.PositiveIntegerField(
#         default=0,
#         validators=[MaxValueValidator(12)],
#         help_text="Количество колонок в строке (0-12) для mobile"
#     )
#     is_active_link = models.BooleanField(default=True, help_text="Активная ссылка")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
#
#     class MPTTMeta:
#         order_insertion_by = ['order']
#
#     class Meta:
#         verbose_name = "Пункт меню"
#         verbose_name_plural = "Меню footer"
#
#     def __str__(self):
#         return self.name
#
#     # --- Вспомогательные методы ---
#     def get_col_desktop(self):
#         """Автоматическая логика колонок"""
#         if self.col_desctop:
#             return self.col_desctop
#         return 4 if self.parent is None and self.order < 4 else 12
#
#     def get_col_md(self):
#         return self.col_md or 12
#
#     def get_url(self):
#         """Формируем реальную ссылку"""
#         if not self.url or self.url == "#":
#             return "#"
#         try:
#             return reverse(self.url, kwargs=self.url_params or {})
#         except NoReverseMatch:
#             return "#"
