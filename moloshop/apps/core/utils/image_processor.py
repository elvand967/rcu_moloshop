
# apps/core/utils/image_processor.py

# from apps.core.utils.image_processor import process_image, ImageSpec

import os
import hashlib
import random
from io import BytesIO
from dataclasses import dataclass
from typing import Optional
from PIL import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify

COLOR_PALETTES = [
    ("#1abc9c", "#ffffff"),
    ("#3498db", "#ffffff"),
    ("#9b59b6", "#ffffff"),
    ("#e67e22", "#ffffff"),
    ("#e74c3c", "#ffffff"),
    ("#2c3e50", "#ecf0f1"),
    ("#16a085", "#ffffff"),
]

def random_color(seed: Optional[str] = None):
    if seed:
        index = int(hashlib.sha256(seed.encode("utf-8")).hexdigest(), 16)
        return COLOR_PALETTES[index % len(COLOR_PALETTES)][0]
    return random.choice(COLOR_PALETTES)[0]

@dataclass
class ImageSpec:
    width: int | None = None      # требуемая ширина
    height: int | None = None     # требуемая высота
    aspect_ratio: float | None = None  # сохранить/привести к пропорциям (например, 16/9)
    crop: bool = True             # обрезать до пропорций
    center: tuple[float, float] = (0.5, 0.5)  # центр кадра (x, y) [0..1]
    fill_transparency: bool = True  # заливать фон если есть прозрачность
    bg_color: str | None = None   # цвет фона (если None → случайный из палитры)
    min_size: bool = False        # требовать min ширину/высоту (иначе — растягиваем)
    formats: list[str] = None     # форматы сохранения ["JPEG", "WEBP", ...]
    quality: int = 85             # качество сохранения
    slug_seed: str | None = None  # строка для генерации имени файла
    base_dir: str = ""            # относительный путь (например avatars/, products/, headers/)

def process_image(file_field, spec: ImageSpec):
    try:
        file_field.seek(0)
        img = Image.open(BytesIO(file_field.read()))

        # Обработка прозрачности
        if spec.fill_transparency and "A" in img.getbands():
            alpha = img.getchannel("A")
            if alpha.getextrema()[0] < 255:
                bg_color = spec.bg_color or random_color(spec.slug_seed or "default")
                bg = Image.new("RGBA", img.size, bg_color)
                bg.paste(img, mask=alpha)
                img = bg

        img = img.convert("RGB")

        # Приведение к нужному размеру/пропорциям
        if spec.width and spec.height:
            target_ratio = spec.width / spec.height
            src_w, src_h = img.size
            src_ratio = src_w / src_h

            if spec.crop:
                if src_ratio > target_ratio:
                    # слишком широкое → обрезаем по ширине
                    new_width = int(src_h * target_ratio)
                    x = int((src_w - new_width) * spec.center[0])
                    img = img.crop((x, 0, x + new_width, src_h))
                elif src_ratio < target_ratio:
                    # слишком высокое → обрезаем по высоте
                    new_height = int(src_w / target_ratio)
                    y = int((src_h - new_height) * spec.center[1])
                    img = img.crop((0, y, src_w, y + new_height))

            img = img.resize((spec.width, spec.height), Image.LANCZOS)

        # Имя файла
        safe_slug = slugify(spec.slug_seed or "image")
        suffix = hashlib.sha1((spec.slug_seed or "img").encode()).hexdigest()[:8]
        base_name = os.path.join(spec.base_dir, f"{safe_slug}-{suffix}")

        # Сохранение в форматы
        results = {}
        for fmt in (spec.formats or ["JPEG"]):
            ext = fmt.lower()
            buffer = BytesIO()
            img.save(buffer, format=fmt, quality=spec.quality)
            results[ext] = ContentFile(buffer.getvalue(), name=f"{base_name}.{ext}")

        return results

    except Exception as e:
        print(f"Ошибка обработки изображения: {e}")
        return None
