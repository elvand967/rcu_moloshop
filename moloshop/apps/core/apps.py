
# ../apps/core/apps.py

from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Общие утилиты, миксины, базовые модели'
    verbose_name_plural = 'Общие утилиты, миксины, базовые модели'

    def ready(self):
        import apps.core.signals  # автоматически подгрузит slug_signals и media_signals