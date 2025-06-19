from django.contrib.auth import validators
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError


class UsernameValidator(validators.UnicodeUsernameValidator):
    regex = settings.USERNAME_REGEX
    message = _(
        f"Enter a valid username. This value may match the regex {regex}."
    )

    def __call__(self, value):
        if value in settings.RESERVED_USERNAMES:
            raise ValidationError(
                _("The current username is on the blocklist."),
                code=self.code,
                params={"value": value}
            )
        super().__call__(value)
