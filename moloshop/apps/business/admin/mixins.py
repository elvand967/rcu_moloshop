# apps/business/admin/mixins.py

from django.urls import reverse
from django.utils.html import format_html
from apps.business.models import Category

'''
Миксин — это такой "набор методов", который можно подключать к разным админкам.
В нём лежит общая логика (business_link, image_preview, formfield_for_foreignkey).
Теперь, если нужно что-то поменять (например, стиль превью или фильтрацию категорий) — мы меняем один файл, 
и изменения применятся ко всем админкам.
Код админок (GoodsAdmin, ServiceAdmin) стал чище и короче.
'''

class BusinessRelatedAdminMixin:
    """
    Миксин для админки товаров и услуг.
    Содержит общую логику:
    - ссылка на бизнес
    - превью изображения
    - фильтрация категорий по бизнесу (категории текущего бизнеса)
    """

    # --- Общие методы ---

    def business_link(self, obj):
        """Возвращает ссылку на связанный бизнес (или прочерк, если нет)."""
        if not obj.business:
            return "—"
        url = reverse("admin:business_business_change", args=[obj.business.pk])
        return format_html('<a href="{}">{}</a>', url, obj.business.title)

    business_link.short_description = "Бизнес"
    business_link.admin_order_field = "business__title"

    def image_preview(self, obj):
        """Показывает мини-превью картинки (если есть)."""
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
        """
        Фильтруем категории:
        - для существующего объекта показываем только категории его бизнеса,
        - для нового объекта пока бизнес неизвестен → пустой список.
        """
        if db_field.name == "category":
            object_id = request.resolver_match.kwargs.get("object_id")
            model = self.model  # получаем модель (Goods или Service)
            if object_id:
                try:
                    obj = model.objects.get(pk=object_id)
                    kwargs["queryset"] = Category.objects.filter(
                        business=obj.business
                    ).order_by("title")
                except model.DoesNotExist:
                    kwargs["queryset"] = Category.objects.none()
            else:
                kwargs["queryset"] = Category.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
