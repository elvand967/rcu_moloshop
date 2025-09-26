
# apps/business/admin/media.py

import nested_admin
from django.contrib import admin
from django.utils.html import format_html
from apps.business.models.business_products import Media
from django.contrib.contenttypes.admin import GenericTabularInline


class MediaInline(nested_admin.NestedGenericTabularInline):
    model = Media
    extra = 1
    readonly_fields = ('image_preview',)
    fields = ('file', 'image_preview', 'alt_text', 'order', 'is_main')

    def image_preview(self, obj):
        if obj.file:
            return format_html(
                '<img src="{}" style="max-height:50px; border-radius:4px;" />',
                obj.file.url
            )
        return "—"
    image_preview.short_description = "Превью"
