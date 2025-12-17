from django.core import validators
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class UsernameValidator(UnicodeUsernameValidator):
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


@deconstructible
class OrganizationNameValidator(validators.RegexValidator):
    regex = settings.ORGANIZATION_NAME_REGEX
    message = _(
        f"Enter a valid organization name. This value may match the regex {regex}."
    )
    flags = 0
