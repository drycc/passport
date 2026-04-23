"""
Helper functions used by the Drycc Passport server.
"""
import re
import logging
import datetime

import requests
from django.conf import settings

from urllib.parse import urlencode

from django.utils.html import strip_tags
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render

from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


def timestamp2datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def login_required(
        required=True, json_stream=True, has_version=True,
        methods=["GET", "POST", "PUT", "DELETE", "PATCH"]):
    def _login_required(view):
        def __decorator(request, *args, **kwargs):
            if request.method not in methods:
                return view(request, *args, **kwargs)
            if not request.user.pk or not request.user.is_authenticated:
                return render(request, 'user/login.html')
            else:
                return view(request, *args, **kwargs)

        return __decorator

    return _login_required


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"


token_generator = TokenGenerator()


def get_local_host(request):
    uri = request.build_absolute_uri()
    return uri[0:uri.find(request.path)]


def get_user_socials(user):
    from api.apps_extra.social_core import backends
    provider_map = {
        backend_cls.name: backend_cls
        for backend_cls in backends.__all__
    }
    results = []
    for social in user.social_auth.all():
        backend_cls = provider_map.get(social.provider)
        email = None
        if social.extra_data:
            email = social.extra_data.get('email') or social.extra_data.get('user_email')
        results.append({
            'id': social.id,
            'provider': social.provider,
            'display_name': social.provider.title(),
            'uid': social.uid,
            'icon': backend_cls.icon if backend_cls else '',
            'email': email or user.email,
        })
    return results


def get_oauth_callback(request, status, provider=None):
    query = {'status': status}
    domain = get_local_host(request)
    if provider:
        query['provider'] = provider
    return f"{domain}{settings.SOCIAL_AUTH_LOGIN_CALLBACK_URL}?{urlencode(query)}"


def validate_reserved_names(value):
    """A value cannot use some reserved names."""
    for reserved_name_pattern in settings.RESERVED_NAME_PATTERNS:
        if re.match(reserved_name_pattern, value):
            raise ValidationError('{} is a reserved name.'.format(value))


def send_activation_email(request, user):
    if not user.email:
        logger.warning(
            "Activation email skipped for user %s due to missing email address",
            user.username
        )
        return
    if not getattr(settings, 'EMAIL_HOST', ''):
        logger.warning(
            "Activation email skipped for user %s due to missing SMTP configuration",
            user.username
        )
        return
    domain = get_local_host(request)
    mail_subject = 'Activate your account.'
    message = render_to_string(
        'user/account_activation_email.html', {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        })
    user.email_user(mail_subject, message, fail_silently=True)


def send_email_notification(message) -> None:
    """Send an email notification for a message.

    Silently skips when SMTP / DEFAULT_FROM_EMAIL is not configured, or
    when the target user has no email address. This avoids triggering
    endless Celery retries in environments without a configured mail
    server (e.g. local development).
    """
    if message.user.email is None:
        logger.info(
            "Email notification skipped for message %s due to missing user email",
            message.id
        )
        return
    if not getattr(settings, 'EMAIL_HOST', ''):
        logger.info(
            "Email notification skipped for message %s due to missing SMTP configuration",
            message.id
        )
        return
    mail_subject = f"[{message.get_category_display()}] {message.title}"
    html_message = render_to_string(
        'notifications/email_message.html',
        {
            'message': message,
            'user': message.user,
            'domain': getattr(settings, 'DASHBOARD_URL', '/'),
        }
    )
    plain_message = strip_tags(html_message)
    message.user.email_user(
        subject=mail_subject,
        message=plain_message,
        html_message=html_message,
        fail_silently=False,
    )
    logger.info("Email notification sent to %s for message %s", message.user.email, message.id)


def send_webhook_notification(message, webhook_url) -> None:
    """Send a webhook notification for a message."""
    if not webhook_url:
        return
    payload = {
        'id': str(message.id),
        'category': message.category,
        'title': message.title,
        'content': message.content,
        'severity': message.severity,
        'created_at': message.created_at.isoformat() if message.created_at else None,
        'user': {
            'id': message.user.id,
            'username': message.user.username,
            'email': message.user.email,
        },
    }
    response = requests.post(
        webhook_url,
        json=payload,
        headers={'Content-Type': 'application/json'},
        timeout=10,
    )
    response.raise_for_status()
    logger.info("Webhook notification sent for message %s to %s", message.id, webhook_url)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
