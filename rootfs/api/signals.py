from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from api.models import Message

User = get_user_model()


@receiver(post_save, sender=Message)
def message_changed_handle(sender, instance, created, **kwargs):
    """Queue async notification dispatch when a new message is created."""
    if created:
        from api.tasks import send_notification
        send_notification.delay(instance)
