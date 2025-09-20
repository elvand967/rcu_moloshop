# ../apps/core/admin/core_documents.py

from django.contrib import admin
from ..models.core_documents import ContractsInstructions


@admin.register(ContractsInstructions)
class ContractsInstructionsAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "namespace", "created_at")
    list_filter = ("namespace", "created_at")
    search_fields = ("title", "slug", "seo_title", "seo_description")
    # prepopulated_fields = {"slug": ("title",)}  # автоподстановка slug из title
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {
            "fields": ("title", "namespace", "slug", "content")
        }),
        ("SEO", {
            "fields": ("seo_title", "seo_description"),
            "classes": ("collapse",),  # можно свернуть блок
        }),
        ("Служебное", {
            "fields": ("created_at",),
        }),
    )
