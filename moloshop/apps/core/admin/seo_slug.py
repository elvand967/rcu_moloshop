
# ../apps/core/admin/seo_slug.py

from django.contrib import admin
from apps.core.models.seo import StopWord, SEOReplacement


@admin.register(StopWord)
class StopWordAdmin(admin.ModelAdmin):
    list_display = ("word", "lang")
    search_fields = ("word", "lang")
    list_filter = ("lang",)


@admin.register(SEOReplacement)
class SEOReplacementAdmin(admin.ModelAdmin):
    list_display = ("source_word", "replacement")
    search_fields = ("source_word", "replacement")



