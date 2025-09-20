
# apps/users/utils/avatar.py

import os
import hashlib
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings

# Контрастные пары (bg_color, text_color)
COLOR_PALETTES = [
    ("#1abc9c", "#ffffff"),  # бирюза + белый
    ("#3498db", "#ffffff"),  # синий + белый
    ("#9b59b6", "#ffffff"),  # фиолетовый + белый
    ("#e67e22", "#ffffff"),  # оранжевый + белый
    ("#e74c3c", "#ffffff"),  # красный + белый
    ("#2c3e50", "#ecf0f1"),  # тёмно-синий + светло-серый
    ("#16a085", "#ffffff"),  # тёмная бирюза + белый
    ("#f39c12", "#ffffff"),  # жёлто-оранжевый + белый
    ("#27ae60", "#ffffff"),  # зелёный + белый
    ("#8e44ad", "#ffffff"),  # насыщенный фиолетовый + белый
    ("#c0392b", "#ffffff"),  # бордовый + белый
    ("#34495e", "#ecf0f1"),  # графитовый + светло-серый
    ("#d35400", "#ffffff"),  # ярко-оранжевый + белый
    ("#7f8c8d", "#ffffff"),  # серо-бирюзовый + белый
    ("#2980b9", "#ffffff"),  # ярко-синий + белый
    ("#2ecc71", "#ffffff"),  # ярко-зелёный + белый
    ("#ff6f61", "#ffffff"),  # коралловый + белый
    ("#6c5ce7", "#ffffff"),  # индиго + белый
    ("#ff9ff3", "#2d3436"),  # розовый пастель + графит
    ("#00cec9", "#ffffff"),  # яркая бирюза + белый
    ("#fab1a0", "#2d3436"),  # персиковый + графит
    ("#e84393", "#ffffff"),  # ярко-розовый + белый
    ("#55efc4", "#2d3436"),  # мятный + графит
    ("#ffeaa7", "#2d3436"),  # мягкий жёлтый + графит
    ("#fd79a8", "#ffffff"),  # малиновый + белый
    ("#636e72", "#ecf0f1"),  # тёмно-серый + светло-серый
    ("#a29bfe", "#2d3436"),  # нежно-фиолетовый + графит
    ("#00b894", "#ffffff"),  # морская волна + белый
    ("#fdcb6e", "#2d3436"),  # янтарный + графит
    ("#e17055", "#ffffff"),  # терракотовый + белый
    ("#0984e3", "#ffffff"),  # ярко-голубой + белый
    ("#dfe6e9", "#2d3436"),  # светло-серый + графит
]

def random_colors(seed: str | None = None):
    if seed:
        index = int(hashlib.sha256(seed.encode("utf-8")).hexdigest(), 16)
        return COLOR_PALETTES[index % len(COLOR_PALETTES)]
    return random.choice(COLOR_PALETTES)

def generate_avatar_text(user):
    first_name = getattr(user, "first_name", "")
    last_name = getattr(user, "last_name", "")
    email = getattr(user, "email", "")
    if first_name and last_name:
        return f"{first_name[0].upper()}{last_name[0].upper()}"
    if first_name:
        return first_name[0].upper()
    if email and len(email) >= 2:
        return f"{email[0].upper()}{email[1].lower()}"
    if email:
        return email[0].upper()
    return "?"

def avatar_upload_to(instance, filename):
    date = getattr(instance.user, "date_joined", timezone.now())
    year = date.year
    month = f"{date.month:02d}"
    ext = "jpg"
    return os.path.join("avatars", str(year), str(month), f"{instance.user.id}.{ext}")

def generate_avatar_image(user, size=70):
    text = generate_avatar_text(user)
    bg_color, text_color = random_colors(seed=user.email or str(user.pk))
    img = Image.new("RGB", (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(os.path.join(settings.BASE_DIR, "static/fonts/DejaVuSans-Bold.ttf"), size // 2)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) / 2, (size - text_height) / 2 - text_height * 0.23)
    draw.text(position, text, font=font, fill=text_color)
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=90)
    return ContentFile(buffer.getvalue(), name=f"avatar_{user.pk}.jpg")

def resize_and_crop_center(img, size=70):
    img = img.convert("RGB")
    w, h = img.size
    ratio = w / h
    if 0.8 <= ratio <= 1.2:
        scale = size / min(w, h)
        new_w, new_h = int(w * scale), int(h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - size) // 2
        top = (new_h - size) // 2
    else:
        scale = size / min(w, h)
        new_w, new_h = int(w * scale), int(h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - size) // 2
        top = max(int(new_h * 0.33 - size / 2), 0)
    right = left + size
    bottom = top + size
    return img.crop((left, top, right, bottom))

def process_uploaded_avatar(file_field, user, size=70):
    try:
        file_field.seek(0)
        img = Image.open(BytesIO(file_field.read())).convert("RGBA")
        if "A" in img.getbands():
            alpha = img.getchannel("A")
            if alpha.getextrema()[0] < 255:
                bg_color, _ = random.choice(COLOR_PALETTES)
                bg = Image.new("RGBA", img.size, bg_color)
                bg.paste(img, mask=alpha)
                img = bg
        img = resize_and_crop_center(img, size=size)
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        base_name = getattr(file_field, "name", "avatar").rsplit(".", 1)[0]
        return ContentFile(buffer.getvalue(), name=f"{base_name}.jpg")
    except Exception as e:
        print(f"Ошибка обработки аватарки: {e}")
        return file_field

def delete_old_avatar(path_or_name):
    if not path_or_name:
        return
    # если передан абсолютный путь — используем как есть, иначе собираем через MEDIA_ROOT
    if os.path.isabs(path_or_name):
        full_path = path_or_name
    else:
        full_path = os.path.join(settings.MEDIA_ROOT, path_or_name)
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
    except Exception:
        # либо логировать: logger.exception("..."), либо просто молча пропустить
        pass