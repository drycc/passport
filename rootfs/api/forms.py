from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm as _AuthenticationForm

from api.utils import send_activation_email


class AuthenticationForm(_AuthenticationForm):

    def confirm_login_allowed(self, user):
        if not user.is_active and user.last_login is None:
            send_activation_email(self.request, user)
            raise ValidationError(
                _('The account is not activated, please check the activation email.'),
                code="inactive",
            )
        return super().confirm_login_allowed(user)
