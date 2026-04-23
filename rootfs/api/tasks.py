"""Celery tasks for Drycc Passport."""
import logging

from django.conf import settings
from celery import shared_task
from api.utils import send_email_notification, send_webhook_notification
from api.models import MessagePreference

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_notification(self, message) -> None:
    use_email, use_webhook = False, False
    try:
        preference = message.user.message_preference
    except MessagePreference.DoesNotExist:
        use_email = True
        logger.info("Send email notification for message %s without user preference", message.id)
    else:
        if getattr(preference, f"notify_{message.category}", True):
            use_email = preference.email_alerts
            use_webhook = preference.push_alerts and preference.webhook_url
    if use_email and message.user.email and getattr(settings, 'EMAIL_HOST', ''):
        send_email_notification(message)
    if use_webhook:
        send_webhook_notification(message, preference.webhook_url)
