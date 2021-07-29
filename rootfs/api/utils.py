"""
Helper functions used by the Drycc Passport server.
"""
import logging
import six

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache

logger = logging.getLogger(__name__)


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
