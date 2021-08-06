"""
Helper functions used by the Drycc Passport server.
"""
import logging
import six
import datetime

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


account_activation_token = TokenGenerator()


def get_local_host(request):
    uri = request.build_absolute_uri()
    return uri[0:uri.find(request.path)]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
