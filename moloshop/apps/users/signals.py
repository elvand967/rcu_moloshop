
# ../apps/users/slug_signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile
from .utils.avatar import generate_avatar_image


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Создание профиля при регистрации пользователя.
    Генерация дефолтной аватарки один раз.
    """
    if created:
        profile = UserProfile.objects.create(user=instance)
        if not profile.avatar:
            profile.avatar.save(
                f"{instance.id}.jpg",
                generate_avatar_image(instance, size=70),
                save=True
            )


# '''
# Обработка глобального сигнала "post_delete" производится в apps/core/signals/delete_media_signals.py
# по которому удаляются все картинки сущностей любой модели при удалении таковой
# '''
# @receiver(post_delete, sender=UserProfile)
# def delete_avatar_with_profile(sender, instance, **kwargs):
#     """
#     Удаление аватарки при удалении профиля.
#     """
#     from .utils.avatar import delete_old_avatar
#     if instance.avatar:
#         delete_old_avatar(instance.avatar.name)