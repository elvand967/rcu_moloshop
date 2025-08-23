
# ../apps/core/admin/footer_menu.py

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from apps.core.models.footer_menu import FooterMenuCategory
from apps.core.forms.footer_menu import FooterMenuCategoryForm


@admin.register(FooterMenuCategory)
class FooterMenuCategoryAdmin(DraggableMPTTAdmin):
    """
    Админка для управления меню футера
    """
    form = FooterMenuCategoryForm

    mptt_indent_field = "name"
    list_display = (
        "tree_actions",
        "indented_title",
        "is_active_link",
        "url",
        "external_url",
        "get_url_display",
        "order",
        "col_desctop",
        "col_md",
        "updated_at",
    )
    list_display_links = ("indented_title",)
    list_editable = ("is_active_link", "order", "col_desctop", "col_md")
    list_filter = ("is_active_link",)
    search_fields = ("name", "url", "external_url")

    fieldsets = (
        (None, {
            "fields": (
                "parent",
                "name",
                "icon",
                ("url", "url_params"),
                "external_url",
                "is_active_link",
                "order",
            )
        }),
        ("Сетка", {
            "fields": ("col_desctop", "col_md"),
            "description": "Позиционирование элемента футера в кастомной сетке (0-12)",
        }),
    )

    def get_url_display(self, obj):
        return obj.get_url()
    get_url_display.short_description = "Ссылка"

