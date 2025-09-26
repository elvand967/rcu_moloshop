# apps/business/admin/category.py

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from apps.business.models import Category


from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from apps.business.models import Category

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ("tree_actions", "indented_title", "business", "slug")
    list_display_links = ("indented_title",)
    list_filter = ("business",)
    search_fields = ("title", "slug", "business__title")
    ordering = ("business__title", "tree_id", "lft")
