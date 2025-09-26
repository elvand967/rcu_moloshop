
# apps/business/models/business.py


from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.core.models.abstract import NamedSlugModel, UUIDModel

User = get_user_model()


class Business(NamedSlugModel):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="businesses",
        verbose_name="Владелец",
    )
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    # поля использует upload_to для дефолтного пути загрузки.
    favicon = models.ImageField(upload_to="business_favicons/", blank=True, null=True, verbose_name="favicon.ico")
    logo = models.ImageField(upload_to="business_logos/", blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="Общее описание бизнеса")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_visible = models.BooleanField(default=True, verbose_name="Активированный бизнес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        ordering = ["order"]
        verbose_name = "Бизнес"
        verbose_name_plural = "Бизнесы"

    def __str__(self):
        return self.title

    def get_products_url(self):
        return reverse("business:product_list", kwargs={"business_slug": self.slug})

    def get_landings_url(self):
        return reverse("business:landing_list", kwargs={"business_slug": self.slug})

    @property
    def messengers(self):
        return self.contact_info.messengers.all() if self.contact_info else []


class ContactInfo(UUIDModel):
    business = models.OneToOneField(
        Business, on_delete=models.CASCADE, related_name="contact_info"
    )
    location = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Локация", default="Вся Беларусь"
    )
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        return self.address or self.location or str(self.id)


class Messenger(UUIDModel):
    MESSENGER_TYPE_CHOICES = [
        ("phone", "Телефон"),
        ("email", "Email"),
        ("whatsapp", "WhatsApp"),
        ("telegram", "Telegram"),
        ("viber", "Viber"),
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("vk", "ВКонтакте"),
        ("skype", "Skype"),
    ]

    contact_info = models.ForeignKey(
        ContactInfo, on_delete=models.CASCADE, related_name="messengers"
    )
    messenger_type = models.CharField(
        max_length=20, choices=MESSENGER_TYPE_CHOICES, verbose_name="Тип мессенджера"
    )
    identifier = models.CharField(max_length=255, verbose_name="Идентификатор или ссылка")

    class Meta:
        verbose_name = "Мессенджер"
        verbose_name_plural = "Мессенджеры"
        unique_together = ("contact_info", "messenger_type", "identifier")

    def __str__(self):
        return f"{self.get_messenger_type_display()}: {self.identifier}"