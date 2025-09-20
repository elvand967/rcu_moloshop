
# ../apps/users/apps.py

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'Пользователи'
    verbose_name_plural = 'Пользователи'

    def ready(self):
        # Подключаем сигналы
        import apps.users.signals  # noqa