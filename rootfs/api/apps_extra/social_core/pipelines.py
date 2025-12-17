"""
Custom social auth pipeline for OAuth2 binding and creation guidance.
"""

import logging

from django.shortcuts import redirect
from social_django.models import UserSocialAuth

from api.utils import get_oauth_callback

logger = logging.getLogger(__name__)


def handle_authenticated_binding(backend, uid, details, response, *args, **kwargs):
    request = backend.strategy.request
    if not request or not request.user.is_authenticated:
        return None

    current_user = request.user
    try:
        existing_social = UserSocialAuth.objects.filter(
            provider=backend.name, uid=uid
        ).select_related('user').first()
        if existing_social and existing_social.user_id != current_user.id:
            return redirect(get_oauth_callback(request, 'conflict', backend.name))
        if existing_social and existing_social.user_id == current_user.id:
            return redirect(get_oauth_callback(request, 'already_linked', backend.name))

        UserSocialAuth.objects.create(
            user=current_user,
            provider=backend.name,
            uid=uid,
            extra_data=response or {}
        )
        return redirect(get_oauth_callback(request, 'linked', backend.name))
    except Exception as exc:
        logger.exception(exc)
        return redirect(get_oauth_callback(request, 'error', backend.name))


def require_username_password(backend, uid, details, response, user=None, *args, **kwargs):
    request = backend.strategy.request
    if request and request.user.is_authenticated:
        return None
    if user:
        return None

    email = details.get('email')
    if not email:
        return redirect(get_oauth_callback(request, 'missing_email', backend.name))

    backend.strategy.session_set('oauth_pending', {
        'provider': backend.name,
        'uid': uid,
        'email': email,
        'extra_data': response or {},
    })
    return redirect(get_oauth_callback(request, 'pending', backend.name))
