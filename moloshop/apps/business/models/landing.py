# apps/business/models/landing.py

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.core.models.abstract import SlugNamespaceModel, UUIDModel
from .business import Business


class Landing(SlugNamespaceModel):
    """
    Лендинг привязан к бизнесу. slug+namespace (namespace=business_id) обеспечивает
    уникальность slug в пространстве бизнеса.
    Наследует title, slug, namespace из SlugNamespaceModel.
    """
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="landings", verbose_name=_("Бизнес")
    )
    # seo_title = models.CharField(max_length=70, blank=True, null=True, verbose_name="SEO заголовок")
    # seo_description = models.CharField(max_length=160, blank=True, null=True, verbose_name="SEO описание бизнеса")
    template = models.CharField(max_length=50, choices=[("default", "Стандарт"), ("modern", "Современный")], default="default")
    content = models.TextField(blank=True, verbose_name=_("Контент лендинга (HTML/JSON)"))
    is_active = models.BooleanField(default=True, verbose_name=_("Опубликован"))
    seo_title = models.CharField(max_length=70, blank=True, null=True)
    seo_description = models.CharField(max_length=160, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создан"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлён"))

    class Meta:
        verbose_name = _("Лендинг")
        verbose_name_plural = _("Лендинги")

    def save(self, *args, **kwargs):
        # namespace = business_id (чтобы slug был уникален per business)
        if not self.namespace and self.business_id:
            self.namespace = str(self.business_id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.business})"

    def get_absolute_url(self):
        return reverse("business:landing_detail", kwargs={"business_slug": self.business.slug, "landing_slug": self.slug})


class Section(UUIDModel):
    """Блок лендинга — заголовок, HTML-контент, порядок и видимость."""
    class BlockType(models.TextChoices):
        HERO = "hero", _("Hero")
        BENEFITS = "benefits", _("Выгоды")
        PRODUCTS = "products", _("Продукты")
        TESTIMONIALS = "testimonials", _("Отзывы")
        FAQ = "faq", _("FAQ")
        CTA = "cta", _("CTA")
        ABOUT = "about", _("О компании")
        CONTACTS = "contacts", _("Контакты")
        CUSTOM = "custom", _("Кастомный")

    landing = models.ForeignKey(Landing, on_delete=models.CASCADE, related_name="sections", verbose_name=_("Лендинг"))
    block_type = models.CharField(max_length=50, choices=BlockType.choices, default=BlockType.CUSTOM, verbose_name=_("Тип блока"))
    title = models.CharField(max_length=255, blank=True, verbose_name=_("Заголовок"))
    content = models.TextField(blank=True, verbose_name=_("Контент (HTML)"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Порядок"))
    is_visible = models.BooleanField(default=True, verbose_name=_("Показывать"))

    class Meta:
        ordering = ["order"]
        verbose_name = _("Секция")
        verbose_name_plural = _("Секции")

    def __str__(self):
        return f"{self.get_block_type_display()} — {self.title or 'без названия'}"


class SectionImage(UUIDModel):
    """Изображения галереи, привязанные к Section."""
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="images", verbose_name=_("Секция"))
    image = models.ImageField(upload_to="landing/sections/", verbose_name=_("Изображение"))
    caption = models.CharField(max_length=255, blank=True, verbose_name=_("Подпись"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Порядок"))

    class Meta:
        ordering = ["order"]
        verbose_name = _("Изображение секции")
        verbose_name_plural = _("Изображения секции")

    def __str__(self):
        return self.caption or f"Image {self.id}"
