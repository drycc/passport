from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from oauth2_provider.models import AbstractApplication


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)


class Application(AbstractApplication):

    def allows_grant_type(self, *grant_types):
        return self.GRANT_AUTHORIZATION_CODE in grant_types or super().allows_grant_type(
            *grant_types
        )
