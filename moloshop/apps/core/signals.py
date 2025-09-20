# ../apps/core/signals.py

from django.db.models.signals import pre_save
from django.db import models
from django.dispatch import receiver
from django.db.models import Q
from apps.core.utils.slugify_seo import slugify_seo


@receiver(pre_save)
def global_slug_autofill(sender, instance, **kwargs):
    if not issubclass(sender, models.Model) or sender._meta.abstract:
        return
    if sender._meta.app_label.startswith("django"):
        return

    if not (hasattr(instance, "slug") and hasattr(instance, "title")):
        return

    # Проверяем, что slug — поле CharField или SlugField
    try:
        slug_field = sender._meta.get_field("slug")
    except Exception:
        return

    if not isinstance(slug_field, (models.SlugField, models.CharField)):
        return

    slug_val = getattr(instance, "slug", None)
    title_val = getattr(instance, "title", None)

    if slug_val or not title_val:
        return

    base_slug = slugify_seo(title_val)
    slug = base_slug

    ModelClass = sender
    namespace_field = "namespace" if hasattr(instance, "namespace") else None

    counter = 1
    while True:
        queryset = ModelClass.objects.filter(slug=slug)

        if namespace_field:
            ns_value = getattr(instance, namespace_field)
            if ns_value in [None, ""]:
                queryset = queryset.filter(Q(namespace__isnull=True) | Q(namespace=""))
            else:
                queryset = queryset.filter(**{namespace_field: ns_value})

        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

        if not queryset.exists():
            break

        slug = f"{base_slug}-{counter}"
        counter += 1

    setattr(instance, "slug", slug)

