# apps/business/utils/image_utils.py

import os
import hashlib
import random
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify  # добавляем slugify

# Максимальная ширина/высота для карточек (16:9)
TARGET_WIDTH = 430
TARGET_HEIGHT = 242

# Цвета для заливки (если есть прозрачность)
COLOR_PALETTES = [
    ("#1abc9c", "#ffffff"),
    ("#3498db", "#ffffff"),
    ("#e67e22", "#ffffff"),
    ("#e74c3c", "#ffffff"),
    ("#9b59b6", "#ffffff"),
    ("#f1c40f", "#ffffff"),
    ("#dfe6e9", "#2d3436"),
]


def random_bg_color(seed: str | None = None):
    if seed:
        index = int(hashlib.sha256(seed.encode("utf-8")).hexdigest(), 16)
        return COLOR_PALETTES[index % len(COLOR_PALETTES)][0]
    return random.choice(COLOR_PALETTES)[0]


def resize_and_crop_16_9(img: Image.Image, width=TARGET_WIDTH, height=TARGET_HEIGHT):
    """
    Приводим изображение к 16:9, центрируем, обрезаем лишнее.
    """
    img = img.convert("RGB")
    src_w, src_h = img.size
    target_ratio = width / height
    src_ratio = src_w / src_h

    # Обрезаем по центру
    if src_ratio > target_ratio:
        # Слишком широкое → обрезаем по ширине
        new_width = int(src_h * target_ratio)
        left = (src_w - new_width) // 2
        img = img.crop((left, 0, left + new_width, src_h))
    elif src_ratio < target_ratio:
        # Слишком высокое → обрезаем по высоте
        new_height = int(src_w / target_ratio)
        top = (src_h - new_height) // 2
        img = img.crop((0, top, src_w, top + new_height))

    # Сжимаем до TARGET_WIDTH x TARGET_HEIGHT
    img = img.resize((width, height), Image.LANCZOS)
    return img


def process_product_image(file_field, business_slug: str, created_at, seed: str | None = None):
    """
    Обработка изображения товара/услуги:
    - приводим к 430x242 (16:9),
    - сохраняем JPEG и WebP,
    - имя файла: <year>/<month>/<business-slug>-<хэш>.jpg / .webp
    """
    try:
        file_field.seek(0)
        img = Image.open(BytesIO(file_field.read()))

        # Если есть прозрачность → заливаем случайным фоном
        if "A" in img.getbands():
            alpha = img.getchannel("A")
            if alpha.getextrema()[0] < 255:
                bg_color = random_bg_color(seed or business_slug)
                bg = Image.new("RGBA", img.size, bg_color)
                bg.paste(img, mask=alpha)
                img = bg

        # Приводим к 16:9 и нужному размеру
        img = resize_and_crop_16_9(img)

        # Дата регистрации бизнеса
        year = created_at.strftime("%Y")
        month = created_at.strftime("%m")

        # Генерация имени файла
        safe_business = slugify(business_slug) or "business"
        suffix = hashlib.sha1((seed or business_slug).encode()).hexdigest()[:8]
        base_name = f"{safe_business}-{suffix}"

        # Относительный путь: year/month/filename
        relative_path = os.path.join(year, month, base_name)

        # JPEG
        buffer_jpg = BytesIO()
        img.save(buffer_jpg, format="JPEG", quality=85)
        content_jpg = ContentFile(buffer_jpg.getvalue(), name=f"{relative_path}.jpg")

        # WebP
        buffer_webp = BytesIO()
        img.save(buffer_webp, format="WEBP", quality=85)
        content_webp = ContentFile(buffer_webp.getvalue(), name=f"{relative_path}.webp")

        return {"jpeg": content_jpg, "webp": content_webp}

    except Exception as e:
        print(f"Ошибка обработки изображения продукта: {e}")
        return None
