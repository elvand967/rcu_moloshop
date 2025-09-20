
# ../apps/core/models/seo.py

from django.db import models
from .abstract import UUIDModel


class StopWord(UUIDModel):
    lang = models.CharField(max_length=5, default="ru", help_text="Код языка, например ru или en")
    word = models.CharField(max_length=50)

    class Meta:
        unique_together = ("lang", "word")
        verbose_name = "SEO-Стоп-слово"
        verbose_name_plural = "SEO-Стоп-слова"

    def __str__(self):
        return f"[{self.lang}] {self.word}"


class SEOReplacement(UUIDModel):
    source_word = models.CharField(max_length=100, unique=True, help_text="Слово или бренд, например айфон")
    replacement = models.CharField(max_length=100, help_text="SEO-замена, например iphone")

    class Meta:
        verbose_name = "SEO-Замена"
        verbose_name_plural = "SEO-Замены"

    def __str__(self):
        return f"{self.source_word} → {self.replacement}"
