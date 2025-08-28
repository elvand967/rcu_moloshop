
# ../apps/users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models.profile import UserProfile
from django.db.models.signals import post_delete



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создаём профиль при создании пользователя."""
    if created and not hasattr(instance, "profile"):
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Обновляем профиль при сохранении пользователя."""
    if hasattr(instance, "profile"):
        instance.profile.save()


@receiver(post_delete, sender=UserProfile)
def delete_avatar_on_profile_delete(sender, instance, **kwargs):
    """
    Удаляем файл аватарки при удалении профиля.
    """
    if instance.avatar:
        instance.avatar.delete(save=False)
