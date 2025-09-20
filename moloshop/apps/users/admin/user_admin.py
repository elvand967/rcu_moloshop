# apps/users/admin/user_admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from ..models import CustomUser, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    classes = ("collapse",)  # сворачиваемая секция
    verbose_name_plural = "Профиль пользователя"


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ("avatar_tag", "email", "first_name", "last_name", "is_active", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)

    # email кликабелен
    list_display_links = ("email",)

    # подключаем оба inline
    inlines = [UserProfileInline]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name"),
                              "classes": ("collapse",),  # аккордеон
                              }),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
                              "classes": ("collapse",),  # аккордеон
                            }),
        (_("Important dates"), {"fields": ("last_login", "date_joined"),
                                "classes": ("collapse",),  # аккордеон
                                }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

    def avatar_tag(self, obj):
        """Отображение миниатюры аватарки в списке пользователей"""
        try:
            if obj.profile.avatar:
                return format_html(
                    '<img src="{}" width="32" height="32" style="border-radius:50%;" />',
                    obj.profile.avatar.url
                )
        except UserProfile.DoesNotExist:
            return "-"
        return "-"
    avatar_tag.short_description = "Аватар"
