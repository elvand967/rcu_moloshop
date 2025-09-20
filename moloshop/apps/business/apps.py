
# apps/business/apps.py

from django.apps import AppConfig


class BusinessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business'  # полный путь до приложения
    verbose_name = 'Бизнес'
    verbose_name_plural = 'Бизнесы'