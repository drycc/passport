from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from oauth2_provider.models import AbstractApplication


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    @property
    def organizations(self) -> list[str]:
        results = []
        if self.is_superuser:
            results.append("admin")
        if self.is_staff:
            results.append("staff")
        if self.is_active:
            results.append(self.username)
        return results


class Application(AbstractApplication):

    def allows_grant_type(self, *grant_types):
        return self.GRANT_AUTHORIZATION_CODE in grant_types or super().allows_grant_type(
            *grant_types
        )
