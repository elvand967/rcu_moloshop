
# apps/business/admin/business.py

import nested_admin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from nested_admin.nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from apps.business.models import Business, ContactInfo, Messenger, Product, Service, Category


# === Inline для продуктов ===
class ProductInline(NestedTabularInline):
    model = Product
    extra = 0
    can_delete = True
    fields = ("title", "sku", "category", "image_preview", "description", "unit", "price", "currency")
    readonly_fields = ("image_preview",)
    show_change_link = True
    classes = ["collapse"]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px; border-radius:4px;" />', obj.image.url)
        return "—"
    image_preview.short_description = "Фото"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            if hasattr(self, "parent_object") and self.parent_object:
                kwargs["queryset"] = Category.objects.filter(business=self.parent_object)
            else:
                kwargs["queryset"] = Category.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# === Inline для услуг ===
class ServiceInline(NestedTabularInline):
    model = Service
    extra = 0
    can_delete = True
    fields = ("title", "sku", "category", "image_preview", "description", "unit", "price",
              "currency", "staff", "place_of_service", "duration", "is_active")
    readonly_fields = ("image_preview",)
    show_change_link = True
    classes = ["collapse"]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px; border-radius:4px;" />', obj.image.url)
        return "—"
    image_preview.short_description = "Фото"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            if hasattr(self, "parent_object") and self.parent_object:
                kwargs["queryset"] = Category.objects.filter(business=self.parent_object)
            else:
                kwargs["queryset"] = Category.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# === Inline для мессенджеров ===
class MessengerInline(NestedTabularInline):
    model = Messenger
    extra = 1
    fk_name = "contact_info"
    fields = ("messenger_type", "identifier")
    show_change_link = True


# === Inline для контактной информации ===
class ContactInfoInline(NestedStackedInline):
    model = ContactInfo
    extra = 0
    can_delete = True
    fields = ("location", "address")
    inlines = [MessengerInline]
    show_change_link = True
    classes = ["collapse"]


# === Админка бизнеса ===
class BusinessAdmin(NestedModelAdmin):
    list_display = ("title", "business_owner", "image_preview", "is_visible",
                    "products_count", "services_count", "created_at")
    list_filter = ("is_visible", "created_at")
    search_fields = ("title", "slug", "description", "owner__email", "owner__first_name", "owner__last_name")
    readonly_fields = ("image_preview",)
    fieldsets = (
        (None, {"fields": ("image_preview", "title", "slug", "owner", "is_visible")}),
        ("Дополнительно", {"classes": ("collapse",), "fields": ("subtitle", "description", "favicon", "logo")}),
    )
    list_editable = ("is_visible",)
    ordering = ("owner__last_name", "title", "created_at")
    inlines = [ContactInfoInline, ProductInline, ServiceInline]

    def get_inline_instances(self, request, obj=None):
        for inline in self.inlines:
            inline.parent_object = obj
        return super().get_inline_instances(request, obj)

    def business_owner(self, obj):
        if not obj.owner:
            return "—"
        owner = obj.owner
        full_name = f"{owner.last_name} {owner.first_name}".strip()
        display_name = f"{full_name} ({owner.email})" if full_name else owner.email or "Без имени"
        url = reverse("admin:users_customuser_change", args=[owner.pk])
        return format_html('<a href="{}">{}</a>', url, display_name)
    business_owner.short_description = "Владелец"
    business_owner.admin_order_field = "owner__last_name"

    def image_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height:50px; border-radius:4px; margin-left:10px;" />', obj.logo.url)
        return "—"
    image_preview.short_description = "Логотип"

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = "Товаров"

    def services_count(self, obj):
        return obj.services.count()
    services_count.short_description = "Услуг"


admin.site.register(Business, BusinessAdmin)
