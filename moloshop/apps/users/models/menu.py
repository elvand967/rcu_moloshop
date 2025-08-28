# # ../apps/users/models/menu.py
#
# from django.db import models
# from unidecode import unidecode
#
# from apps.core.models import UUIDModel
# from mptt.models import MPTTModel, TreeForeignKey
# from django.utils.text import slugify
#
#
# class ProfileMenuCategory(UUIDModel, MPTTModel):
#     """
#     Древовидная модель меню личного кабинета.
#     Хранит имя пункта меню, путь (url_name), slug и параметры для reverse().
#     """
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(
#         unique=True,
#         max_length=100,
#         blank=True,
#         help_text="Автоматически создаётся из названия. Используется для URL-конфигурации."
#     )
#     url = models.CharField(
#         max_length=200,
#         blank=True,
#         help_text="Имя URL-шаблона с namespace (например: 'landing:policy_detail') или абсолютная ссылка"
#     )
#     url_params = models.JSONField(
#         blank=True,
#         null=True,
#         help_text="Параметры для reverse(), например: {'slug': 'privacy-policy'}"
#     )
#     is_named_url = models.BooleanField(default=True, help_text="True — использовать reverse() по url_name")
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
#     order = models.PositiveIntegerField(default=0)
#
#     class MPTTMeta:
#         order_insertion_by = ['order']
#
#     def save(self, *args, **kwargs):
#         if not self.slug and self.name:
#             self.slug = slugify(unidecode(self.name))
#         super().save(*args, **kwargs)
#
#     class Meta:
#         app_label = 'userpanel'
#         verbose_name = "Пункт меню"
#         verbose_name_plural = "Меню личного кабинета"
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         from django.urls import reverse
#         if self.is_named_url:
#             try:
#                 if self.url_params:
#                     return reverse(self.url, kwargs=self.url_params)
#                 return reverse(self.url)
#             except:
#                 return '#'
#         return self.url
