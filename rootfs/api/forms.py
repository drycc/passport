import requests
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as _AuthenticationForm

from api.utils import send_activation_email

User = get_user_model()


class AuthenticationForm(_AuthenticationForm):

    def confirm_login_allowed(self, user):
        if not user.is_active and user.last_login is None:
            send_activation_email(self.request, user)
            raise ValidationError(
                _('The account is not activated, please check the activation email.'),
                code="inactive",
            )
        return super().confirm_login_allowed(user)


class RegistrationForm(UserCreationForm):

    h_captcha_token = forms.CharField(
        label=_("h-captcha token"),
        widget=forms.HiddenInput(attrs={"name": "h-captcha-response"}),
        strip=False,
        required=False,
        help_text=_("Google recaptcha token hidden field"),
    )

    def clean_h_captcha_token(self):
        h_captcha_token = self.data.get("h-captcha-response")
        if settings.H_CAPTCHA_KEY and settings.H_CAPTCHA_SECRET:
            success = requests.post('https://hcaptcha.com/siteverify', data={
                'secret': settings.H_CAPTCHA_SECRET,
                'response': h_captcha_token,
            }).json()["success"]
            if not success:
                raise ValidationError(
                    _('Error verifying HCAPTCHA, please try again.'),
                    code="captcha_invalid",
                )
        return h_captcha_token

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
