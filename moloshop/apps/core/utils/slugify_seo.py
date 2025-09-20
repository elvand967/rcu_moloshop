
# ../apps/core/utils/slugify_seo.py

import re
import uuid
from django.utils.text import slugify
from unidecode import unidecode
from django.core.cache import cache

def load_stop_words():
    """Загрузка стоп-слов из БД с кешированием."""
    from apps.core.models.seo import StopWord
    stop_words = {}
    for sw in StopWord.objects.all():
        stop_words.setdefault(sw.lang, []).append(sw.word.lower())
    cache.set("STOP_WORDS", stop_words, 60 * 60)  # кеш 1 час
    return stop_words

def load_replacements():
    """Загрузка SEO-замен из БД с кешированием."""
    from apps.core.models.seo import SEOReplacement
    replacements = {r.source_word.lower(): r.replacement for r in SEOReplacement.objects.all()}
    cache.set("SEO_REPLACEMENTS", replacements, 60 * 60)
    return replacements

def get_stop_words():
    return cache.get("STOP_WORDS") or load_stop_words()

def get_replacements():
    return cache.get("SEO_REPLACEMENTS") or load_replacements()


def soft_transliterate(text, allow_unicode=False):
    """Мягкая SEO-конверсия: сначала замены, потом транслитерация."""
    replacements = get_replacements()
    for ru_word, seo_word in replacements.items():
        text = re.sub(rf"\b{ru_word}\b", seo_word, text, flags=re.IGNORECASE)

    if allow_unicode:
        return text
    return unidecode(text)


def slugify_seo(text, stop_langs=("ru", "en"), max_length=255, allow_unicode=False):
    if not text:
        return str(uuid.uuid4())[:8]

    text = text.lower().strip()

    # Убираем стоп-слова
    stop_words = get_stop_words()
    for lang in stop_langs:
        words = stop_words.get(lang, [])
        if words:
            text = re.sub(rf"\b({'|'.join(map(re.escape, words))})\b", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    text = soft_transliterate(text, allow_unicode=allow_unicode)

    slug = slugify(text, allow_unicode=allow_unicode)

    return slug[:max_length]

