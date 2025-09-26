
# apps/core/models/abstract.py

from django.db import models
import uuid
from apps.core.utils.slugify_seo import slugify_seo


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


'''Абстрактная модель с UUID,
полями title и глобальной автогенерацией SEO-эффективного slug (без стоп-слов).
Поле slug - уникально в пределах модели'''
class NamedSlugModel(UUIDModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify_seo(self.title)
            self.slug = self.make_unique_slug(base_slug)
        super().save(*args, **kwargs)

    def make_unique_slug(self, base_slug):
        """
        Обеспечивает уникальность slug для конкретной модели.
        """
        ModelClass = self.__class__
        slug = base_slug
        counter = 1
        while ModelClass.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug


'''Абстрактная модель с UUID,
полями title и глобальной автогенерацией SEO-эффективного slug (без стоп-слов).
Пара 'slug + namespace' - уникальна в пределах модели'''
class SlugNamespaceModel(UUIDModel):
    title = models.CharField(max_length=255)
    namespace = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Пространство имён для slug (опционально)"
    )
    slug = models.SlugField(max_length=255, blank=True)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["slug"],
                condition=models.Q(namespace__isnull=True) | models.Q(namespace=""),
                name="unique_slug_global_when_no_namespace"
            ),
            models.UniqueConstraint(
                fields=["namespace", "slug"],
                condition=models.Q(namespace__isnull=False) & ~models.Q(namespace=""),
                name="unique_slug_per_namespace"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify_seo(self.title)
            self.slug = self.make_unique_slug(base_slug)
        super().save(*args, **kwargs)

    def make_unique_slug(self, base_slug):
        ModelClass = self.__class__
        slug = base_slug
        counter = 1

        filters = {"slug": slug}
        if self.namespace:
            filters["namespace"] = self.namespace
        else:
            filters["namespace__isnull"] = True

        while ModelClass.objects.filter(**filters).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            filters["slug"] = slug

        return slug
