
# apps/business/admin/landing.py

from django.contrib import admin
from nested_admin.nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from apps.business.models import Landing, Section, SectionImage


class SectionImageInline(NestedTabularInline):
    model = SectionImage
    extra = 1


class SectionInline(NestedStackedInline):
    model = Section
    extra = 1
    inlines = [SectionImageInline]


@admin.register(Landing)
class LandingAdmin(NestedModelAdmin):
    list_display = ("id", "business", "title")
    search_fields = ("title", "business__title")
    inlines = [SectionInline]

