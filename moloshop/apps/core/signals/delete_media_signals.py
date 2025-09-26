
# apps/core/signals/delete_media_signals.py

import logging
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


@receiver(post_delete)
def delete_media_files_on_delete(sender, instance, **kwargs):
    """
    Универсальный сигнал:
    При удалении объекта любой модели проекта автоматически удаляет
    все связанные медиафайлы (FileField / ImageField), если они реально существуют в storage.
    """

    # --- 1) Исключаем системные/абстрактные модели ---
    # Абстрактные модели не создают таблицы в БД, поэтому файлов у них быть не может
    if not issubclass(sender, models.Model) or sender._meta.abstract:
        return

    # Пропускаем внутренние модели Django (auth, admin и т.д.),
    # т.к. они не содержат наших файлов
    if sender._meta.app_label.startswith("django"):
        return

    # --- 2) Перебираем все поля модели ---
    for field in sender._meta.get_fields():

        # Нас интересуют только поля, которые реально содержат путь к файлу
        # (ImageField наследуется от FileField, поэтому он тоже попадёт сюда)
        if isinstance(field, models.FileField):

            # --- 3) Получаем значение поля (сам FileField объекта) ---
            file_field = getattr(instance, field.name, None)

            # --- 4) Проверяем, что в поле действительно был указан файл ---
            if file_field and file_field.name:

                # --- 5) Проверяем наличие файла в storage ---
                if default_storage.exists(file_field.name):
                    # ✅ Файл существует → удаляем его
                    default_storage.delete(file_field.name)
                    logger.info(
                        "Удалён файл '%s' для поля '%s' модели '%s'",
                        file_field.name, field.name, sender.__name__
                    )
                else:
                    # ⚠️ Запись в БД есть, но самого файла в storage нет
                    logger.warning(
                        "Файл '%s' для поля '%s' модели '%s' отсутствует в storage",
                        file_field.name, field.name, sender.__name__
                    )
