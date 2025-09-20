
# apps/business/admin/service.py

# apps/business/admin/service.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from apps.business.models import Service, Category

class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "business_link", "image_preview", "unit", "price", "currency", "staff", "is_active", "created_at")
    readonly_fields = ("image_preview",)
    list_filter = ("business", "unit", "currency", "staff", "is_active", "created_at")
    search_fields = ("title", "description", "business__title", "staff__user__email")
    ordering = ("business__title", "title")

    def business_link(self, obj):
        if not obj.business:
            return "—"
        url = reverse("admin:business_business_change", args=[obj.business.pk])
        return format_html('<a href="{}">{}</a>', url, obj.business.title)
    business_link.short_description = "Бизнес"
    business_link.admin_order_field = "business__title"

    def image_preview(self, obj):
        style = "max-height:50px; border-radius:4px; margin-left:10px;"
        if obj.image and obj.image_webp:
            html = f'<a href="{obj.image_webp.url}" target="_blank">'
            html += f'<img src="{obj.image.url}" style="{style}" />'
            html += "</a>"
            return format_html(html)
        elif obj.image:
            return format_html('<img src="{}" style="{}" />', obj.image.url, style)
        return "—"
    image_preview.short_description = "Фото"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            object_id = request.resolver_match.kwargs.get("object_id")
            if object_id:
                try:
                    obj = Service.objects.get(pk=object_id)
                    kwargs["queryset"] = Category.objects.filter(business=obj.business).order_by("title")
                except Service.DoesNotExist:
                    kwargs["queryset"] = Category.objects.none()
            else:
                kwargs["queryset"] = Category.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Service, ServiceAdmin)