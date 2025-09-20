
# ../apps/core/utils/load_seo_data.py
'''Скрипт первичной загрузки JSON-файла: один со стоп-словами,
другой с SEO-заменами (мягкие SEO-дружественные транслиты и бренды)'''

import json
import os
import sys
import django

# Добавляем корень проекта в PYTHONPATH (подкорректируйте путь, если нужно)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Убедитесь, что путь к settings правильный
django.setup()


from apps.core.models.seo import StopWord, SEOReplacement

def load_stop_words(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        sw, created = StopWord.objects.get_or_create(
            lang=entry["lang"].lower(),
            word=entry["word"].lower()
        )
        if created:
            print(f"Добавлено стоп-слово: [{sw.lang}] {sw.word}")

def load_seo_replacements(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        rep, created = SEOReplacement.objects.get_or_create(
            source_word=entry["source_word"].lower(),
            defaults={"replacement": entry["replacement"].lower()}
        )
        if not created and rep.replacement != entry["replacement"].lower():
            rep.replacement = entry["replacement"].lower()
            rep.save()
            print(f"Обновлена SEO-замена: {rep.source_word} → {rep.replacement}")
        elif created:
            print(f"Добавлена SEO-замена: {rep.source_word} → {rep.replacement}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    load_stop_words(os.path.join(BASE_DIR, "stop_words.json"))
    load_seo_replacements(os.path.join(BASE_DIR, "seo_replacements.json"))
