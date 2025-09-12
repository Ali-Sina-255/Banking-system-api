from typing import Type

from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from loguru import logger

from apps.user_profile.models import Profile
from config.settings.base import AUTH_USER_MODEL


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender: Type[Model], instance: Model, created: bool, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile created for {instance.first_name} {instance.last_name}")


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender: Type[Model], instance: Model, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()
