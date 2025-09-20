# ../apps/users/admin/profile_admin.py

from django.contrib import admin
from ..models.profile import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number_display",
        "phone_number_digits",
        "location",
        "date_of_birth",
        "created_at",
    )
    search_fields = ("user__email","user__first_name","user__last_name","phone_number_display")
    list_filter = ("location","date_of_birth")
    readonly_fields = ("created_at","updated_at","phone_number_digits")
