"""
Helper functions used by the Drycc Passport server.
"""
import logging
import six
import datetime

from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render

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
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


token_generator = TokenGenerator()


def get_local_host(request):
    uri = request.build_absolute_uri()
    return uri[0:uri.find(request.path)]


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
