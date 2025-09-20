# apps/users/admin/menu.py

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from apps.users.forms.profile_menu_category_form import ProfileMenuCategoryForm
from apps.users.models.menu import ProfileMenuCategory


@admin.register(ProfileMenuCategory)
class ProfileMenuCategoryAdmin(DraggableMPTTAdmin):
    """
    Админка для управления меню личного кабинета
    с drag&drop сортировкой и сворачиваемым деревом
    """
    form = ProfileMenuCategoryForm

    mptt_indent_field = "name"

    list_display = (
        "tree_actions",        # стрелочки сворачивания/разворачивания
        "indented_title",      # «ручка» для drag&drop
        "is_active_link",
        "url",
        "external_url",
        "updated_at",
    )
    list_display_links = ("indented_title",)
    list_editable = ("is_active_link",)
    search_fields = ("name", "url", "external_url")
    list_filter = ("is_active_link", "updated_at")

    fieldsets = (
        (None, {
            "fields": (
                "parent",
                "name",
                "is_active_link",
            )
        }),
        ("Ссылка", {
            "fields": (
                "url",
                "url_params",
                "external_url",
            ),
            "description": "Укажите либо Django-URL (из списка), либо внешнюю ссылку."
        }),
        ("Служебное", {
            "fields": ("updated_at",),
        }),
    )
    readonly_fields = ("updated_at",)