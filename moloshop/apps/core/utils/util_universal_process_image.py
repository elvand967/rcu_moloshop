
# apps/core/utils/util_universal_process_image.py
# https://www.perplexity.ai/

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import hashlib
import random

def universal_process_image(
        file_field,
        size: tuple[int, int],  # (width, height)
        crop_center_offset: float = 0.0,  # смещение центра обрезки -1.0 до 1.0
        fill_transparent: bool = True,
        bg_color_seed: str | None = None,
        save_formats: list[str] = ["JPEG"],  # возможные значения "JPEG", "WEBP"
        base_dir: str = "",
        file_name_seed: str = "image",
        quality: int = 85
    ) -> dict | None:
    """
    Универсальная утилита для обработки загружаемых изображений.
    - size: целевой размер (width, height)
    - crop_center_offset: смещение центра обрезки по вертикали или горизонтали (-1.0 до 1.0)
    - fill_transparent: заливать ли прозрачные зоны цветом
    - bg_color_seed: seed для случайного цвета заливки фона
    - save_formats: форматы сохранения (JPEG/WebP)
    - base_dir: базовая директория для пути сохранения
    - file_name_seed: seed для имени файла
    - quality: качество сохранения
    """
    try:
        file_field.seek(0)
        img = Image.open(BytesIO(file_field.read()))

        # Обработка прозрачности при указанной заливке
        if fill_transparent and "A" in img.getbands():
            alpha = img.getchannel("A")
            if alpha.getextrema()[0] < 255:
                COLOR_PALETTES = [
                    ("#1abc9c", "#ffffff"),
                    ("#3498db", "#ffffff"),
                    ("#e67e22", "#ffffff"),
                    ("#e74c3c", "#ffffff"),
                    ("#9b59b6", "#ffffff"),
                    ("#f1c40f", "#ffffff"),
                    ("#dfe6e9", "#2d3436"),
                ]
                if bg_color_seed:
                    index = int(hashlib.sha256(bg_color_seed.encode("utf-8")).hexdigest(), 16)
                    bg_color = COLOR_PALETTES[index % len(COLOR_PALETTES)][0]
                else:
                    bg_color = random.choice([c[0] for c in COLOR_PALETTES])

                bg = Image.new("RGBA", img.size, bg_color)
                bg.paste(img, mask=alpha)
                img = bg

        # Конвертируем в RGB
        img = img.convert("RGB")
        src_w, src_h = img.size
        target_w, target_h = size
        target_ratio = target_w / target_h
        src_ratio = src_w / src_h

        # Обрезка с учетом crop_center_offset
        if abs(src_ratio - target_ratio) < 1e-5:  # Практически равны
            # Просто масштабируем
            img = img.resize((target_w, target_h), Image.LANCZOS)
        else:
            if src_ratio > target_ratio:
                # Шире целевого -> обрезаем по ширине
                new_width = int(src_h * target_ratio)
                left = int((src_w - new_width) / 2 + crop_center_offset * new_width / 2)
                left = max(0, min(left, src_w - new_width))
                img = img.crop((left, 0, left + new_width, src_h))
            else:
                # Выше целевого -> обрезаем по высоте
                new_height = int(src_w / target_ratio)
                top = int((src_h - new_height) / 2 + crop_center_offset * new_height / 2)
                top = max(0, min(top, src_h - new_height))
                img = img.crop((0, top, src_w, top + new_height))
            # Масштабируем до целевого
            img = img.resize((target_w, target_h), Image.LANCZOS)

        # Логика для мелких изображений — можно дополнительно обработать при необходимости
        if src_w < target_w or src_h < target_h:
            pass

        results = {}

        # Формируем относительный путь и имя файла
        relative_dir = base_dir.strip("/ ") if base_dir else "misc"
        suffix = hashlib.sha1(file_name_seed.encode()).hexdigest()[:8]

        for fmt in save_formats:
            fmt_upper = fmt.upper()
            if fmt_upper == "JPEG":
                ext = "jpg"
            else:
                ext = fmt_upper.lower()
            filename = f"{relative_dir}/{file_name_seed}-{suffix}.{ext}"
            buffer = BytesIO()
            img.save(buffer, format=fmt_upper, quality=quality)
            content = ContentFile(buffer.getvalue(), name=filename)
            results[ext] = content

        return results

    except Exception as e:
        print(f"Ошибка универсальной утилиты обработки изображения: {e}")
        return None
