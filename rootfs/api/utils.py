"""
Helper functions used by the Drycc Passport server.
"""
import re
import logging
import datetime

from urllib.parse import urlencode
from django.conf import settings

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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
