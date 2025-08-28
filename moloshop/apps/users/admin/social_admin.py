
# ../apps/users/admin/social_admin.py

from django.contrib import admin
from ..models.social import UserSocialLink

@admin.register(UserSocialLink)
class UserSocialLinkAdmin(admin.ModelAdmin):
    list_display = ("custom_user", "network", "url", "created_at")
    search_fields = ("custom_user__email", "network", "url")
    list_filter = ("network",)