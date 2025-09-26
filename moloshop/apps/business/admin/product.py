# apps/business/admin/product.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from apps.business.models import Product, Category
from .media import MediaInline

class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "business_link", "image_preview", "unit", "price", "currency", "created_at")
    readonly_fields = ("image_preview",)
    list_filter = ("business", "currency", "created_at")
    search_fields = ("title", "description", "business__title")
    ordering = ("business__title", "title")

    inlines = [MediaInline]  # галерея товара

    def business_link(self, obj):
        if obj.business:
            url = reverse("admin:business_business_change", args=[obj.business.pk])
            return format_html('<a href="{}">{}</a>', url, obj.business.title)
        return "—"
    business_link.short_description = "Бизнес"
    business_link.admin_order_field = "business__title"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px; border-radius:4px; margin-left:10px;" />', obj.image.url)
        return "—"
    image_preview.short_description = "Фото"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Product, ProductAdmin)
