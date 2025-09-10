import uuid
from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ContentView(TimeStampedModel):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type")
    )
    object_id = models.UUIDField(verbose_name=_("Object I D"))
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="content_views",
    )
    viewer_ip = models.GenericIPAddressField(
        verbose_name=_("Viewer IP Address"), blank=True, null=True
    )
    last_view = models.DateTimeField(verbose_name=_("Last View"), default=timezone.now)

    class Meta:
        verbose_name = _("Content View")
        verbose_name_plural = _("Content Views")
        unique_together = (("content_type", "object_id", "user", "viewer_ip"),)

    def __str__(self):
        return (
            f"{self.content_type} viewed by "
            f"{self.user.get_full_name if self.user else 'Anonymous'}  From Ip address: {self.viewer_ip} "
        )

    @classmethod
    def record_view(
        cls,
        content_type: Any,
        object_id,
        user: Optional[User],
        viewer_ip: Optional[str],
    ) -> None:
        content_type = ContentType.objects.get_for_model(content_type)
        try:
            view, created = cls.objects.get_or_create(
                content_type=content_type,
                object_id=object_id,
                defaults={
                    "user": user,
                    "viewer_ip": viewer_ip,
                    "last_view": timezone.now(),
                },
            )
            if not created:
                view.last_view = timezone.now()
                view.save()
        except IntegrityError:

            pass
