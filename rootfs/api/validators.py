
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.deconstruct import deconstructible

from api.utils import validate_reserved_names


@deconstructible
class UsernameValidator(UnicodeUsernameValidator):
    regex = settings.USERNAME_REGEX
    message = _(
        f"Enter a valid username. This value may match the regex {regex}."
    )

    def __call__(self, value):
        super().__call__(value)
        validate_reserved_names(value)
