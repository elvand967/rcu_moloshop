
# ../apps/users/models/social.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from . import CustomUser
from ...core.models import UUIDModel

class UserSocialLink(UUIDModel):
    """Социальная ссылка, привязанная к кастомному пользователю."""

    class SocialChoices(models.TextChoices):
        FACEBOOK = "facebook", "Facebook"
        INSTAGRAM = "instagram", "Instagram"
        TELEGRAM = "telegram", "Telegram"
        LINKEDIN = "linkedin", "LinkedIn"
        YOUTUBE = "youtube", "YouTube"
        TIKTOK = "tiktok", "TikTok"
        OTHER = "other", _("Другое")

    custom_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="social_links",
        verbose_name=_("Пользователь")
    )

    network = models.CharField(
        max_length=50,
        choices=SocialChoices.choices,
        verbose_name=_("Социальная сеть")
    )

    url = models.URLField(
        verbose_name=_("Ссылка на профиль соц.сети")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    class Meta:
        verbose_name = _("Социальная ссылка")
        verbose_name_plural = _("Социальные ссылки")
        unique_together = ("custom_user", "network")

    def __str__(self):
        return f"{self.get_network_display()} ({self.custom_user.email})"