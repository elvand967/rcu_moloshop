
# apps/core/utils/loading_media.py

import os
import uuid
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Конфигурация параметров обработки разных типов изображений
UPLOAD_CONFIG = {
    "favicon": {
        "field": "favicon",            # имя поля с загружаемым файлом
        "target_field": "favicon",     # имя поля модели для сохранения
        "size": (64, 64),              # квадратный размер итогового изображения (ширина, высота)
        "format": "PNG",               # формат для сохранения
        "ext": "png",                  # расширение файла
        "quality": 90,                 # качество для оптимизации (для jpeg/webp)
        "folder": lambda instance: f"business/{instance.slug}",  # функция для формирования пути папки сохранения
    },
    "logo": {
        "field": "logo",
        "target_field": "logo",
        "size": (256, 256),            # квадратный размер логотипа
        "format": "PNG",
        "ext": "png",
        "quality": 85,
        "folder": lambda instance: f"business/{instance.slug}",
    },
    "product_jpg": {
        "field": "image",
        "target_field": "image",       # сохраним как оригинал или resized jpg
        "size": (910, 512),
        "format": "JPEG",
        "ext": "jpg",
        "quality": 85,
        "folder": lambda instance: f"business/{instance.business.slug}/products_jpg",
    },
    "product_webp": {
        "field": "image",
        "target_field": "image_webp",  # отдельное поле для WebP
        "size": (910, 512),
        "format": "WEBP",
        "ext": "webp",
        "quality": 80,
        "folder": lambda instance: f"business/{instance.business.slug}/products_webp",
    },
    "banner": {
        "field": "image",
        "target_field": "image_webp",
        "size": (1920, 600),
        "format": "JPEG",
        "ext": "jpg",
        "quality": 85,
        "folder": lambda instance: f"business/{instance.business.slug}/banners",
    },
}

def crop_and_resize_to_aspect(image: Image.Image, target_size: tuple):
    """
    Обрезает изображение по центру к нужному соотношению сторон
    и масштабирует до заданных размеров.

    :param image: Изображение PIL
    :param target_size: Кортеж (ширина, высота) для итогового изображения
    :return: Обработанное изображение PIL
    """
    target_w, target_h = target_size
    target_ratio = target_w / target_h  # Желаемое соотношение сторон итогового изображения
    img_w, img_h = image.size
    img_ratio = img_w / img_h            # Текущее соотношение сторон изображения

    # Если исходное изображение шире по пропорциям, чем целевое — обрезаем по ширине
    if img_ratio > target_ratio:
        new_width = int(target_ratio * img_h)  # вычисляем новую ширину
        left = (img_w - new_width) // 2        # отступ слева для центрирования обрезки
        right = left + new_width
        top = 0
        bottom = img_h
    else:
        # Если изображение выше / уже в пропорциях, обрезаем по высоте
        new_height = int(img_w / target_ratio) # вычисляем новую высоту
        top = (img_h - new_height) // 2        # отступ сверху для центрирования
        bottom = top + new_height
        left = 0
        right = img_w

    cropped = image.crop((left, top, right, bottom))             # обрезаем изображение по рассчитанным координатам
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)  # масштабируем до нужного размера с высоким качеством
    return resized

def process_image(file, instance, image_type: str):
    """
    Универсальная функция обработки изображений с учётом EXIF-ориентации.

    Принимает:
    - file: исходный файл (например, request.FILES[...])
    - instance: объект модели (для получения slug и сохранения пути)
    - image_type: ключ из UPLOAD_CONFIG, определяющий параметры обработки

    Возвращает путь к сохранённому файлу (относительно MEDIA_ROOT).
    """

    config = UPLOAD_CONFIG.get(image_type)
    if not config:
        raise ValueError(f"Unknown image_type '{image_type}'")

    field = config["field"]                        # имя поля исходного файла
    target_field = config.get("target_field", field)  # имя поля для сохранения результата
    size = config["size"]                          # размер для конечного изображения
    fmt = config["format"]                         # формат сохранения
    ext = config["ext"]                            # расширение файла
    quality = config.get("quality", 85)            # качество сохранения
    folder_path = config["folder"](instance)      # путь для сохранения файла

    image = Image.open(file)                        # открываем исходный файл через PIL

    # Коррекция ориентации изображения с учётом EXIF (автоматический поворот)
    image = ImageOps.exif_transpose(image)

    # Приведение к корректному цветовому режиму, если требуется для формата файла
    if fmt == "PNG" and image.mode != "RGBA":
        image = image.convert("RGBA")
    elif fmt in ("JPEG", "WEBP") and image.mode not in ("RGB", "RGBA", "LA"):
        image = image.convert("RGB")

    # Обработка обрезки и масштаба с учетом размера из конфига:
    image = crop_and_resize_to_aspect(image, size)

    # Генерируем уникальное имя файла с использованием uuid для избежания коллизий
    filename = f"{target_field}_{instance.slug}_{uuid.uuid4().hex[:8]}.{ext}"
    path = os.path.join(folder_path, filename)    # полный путь для сохранения файла

    buffer = BytesIO()                             # создаём буфер для временного хранения байтов

    save_kwargs = {"format": fmt}                  # параметры сохранения
    if fmt == "JPEG":
        save_kwargs.update({"quality": quality, "optimize": True})
    elif fmt == "WEBP":
        save_kwargs.update({"quality": quality, "method": 6})
    elif fmt == "PNG":
        save_kwargs.update({"optimize": True})

    image.save(buffer, **save_kwargs)              # сохраняем изображение в буфер с указанными параметрами
    buffer.seek(0)                                 # переносим указатель в начало буфера

    saved_path = default_storage.save(path, ContentFile(buffer.read()))  # сохраняем в файл в хранилище Django

    # Удаляем старый файл, если он существует
    if hasattr(instance, target_field):
        old_file = getattr(instance, target_field)
        if old_file and default_storage.exists(old_file.name):
            try:
                default_storage.delete(old_file.name)
            except Exception:
                pass
        setattr(instance, target_field, saved_path)

    return saved_path  # возвращаем относительный путь к сохранённому файлу