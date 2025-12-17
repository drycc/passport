from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, views
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from social_django.models import UserSocialAuth

from api import serializers
from api.forms import AuthenticationForm, RegistrationForm
from api.utils import get_oauth_callback, send_activation_email, token_generator


User = get_user_model()


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('user_registration_done')

    def get(self, request, *args, **kwargs):
        if settings.LDAP_ENDPOINT or not settings.REGISTRATION_ENABLED:
            return render(request, template_name='user/registration_disable.html')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if settings.LDAP_ENDPOINT or not settings.REGISTRATION_ENABLED:
            return render(request, template_name='user/registration_disable.html')
        form = self.form_class(request.POST)
        self.object = None
        if form.is_valid():
            user = form.save(commit=False)
            if settings.EMAIL_HOST:
                user.is_active = False
                user.save()
                send_activation_email(request, user)
                messages.success(request, 'Please Confirm your email to complete registration.')
            else:
                user.is_active = True
                user.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["h_captcha_key"] = settings.H_CAPTCHA_KEY
        return context


class RegistrationDoneView(TemplateView):
    template_name = 'user/registration_done.html'
    title = _('Activate email sent')


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Your account have been confirmed.')
            return redirect('/user/activate/done/')

        messages.warning(
            request,
            'The confirmation link was invalid, possibly because it has already been used.',
        )
        return redirect('/user/activate/fail/')


class ActivateAccountDoneView(TemplateView):
    template_name = 'user/account_activation_done.html'
    title = _('Activate account done')


class ActivateAccountFailView(TemplateView):
    template_name = 'user/account_activation_fail.html'
    title = _('Activate account fail')


class UserLoginView(views.LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'

    def _get_identity_linking(self):
        identity_linking = self.request.POST.get('identity_linking')
        if identity_linking is None:
            identity_linking = self.request.GET.get('identity_linking')
        return identity_linking == '1'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        identity_linking = self._get_identity_linking()
        form = kwargs.get('form')
        context.update({
            'identity_linking': identity_linking,
            'registration_enabled': settings.REGISTRATION_ENABLED,
            'password_reset_enabled': True if settings.EMAIL_HOST else False,
            'identity_linking_error': (
                _('Identity linking login failed. Please try again.')
                if identity_linking and form is not None and form.errors else None
            ),
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        pending = self.request.session.get('oauth_pending')
        if not pending:
            return response

        provider = pending.get('provider')
        uid = pending.get('uid')
        extra_data = pending.get('extra_data') or {}
        if not provider or not uid:
            self.request.session.pop('oauth_pending', None)
            raise ValidationError('invalid oauth pending data')

        existing = UserSocialAuth.objects.filter(
            provider=provider,
            uid=uid,
        ).select_related('user').first()
        if existing and existing.user_id != self.request.user.id:
            self.request.session.pop('oauth_pending', None)
            return redirect(get_oauth_callback(self.request, 'conflict', provider))

        if not existing:
            UserSocialAuth.objects.create(
                user=self.request.user,
                provider=provider,
                uid=uid,
                extra_data=extra_data,
            )

        self.request.session.pop('oauth_pending', None)
        return redirect(get_oauth_callback(self.request, 'linked', provider))


class OAuthCallbackTemplateView(TemplateView):
    template_name = 'user/oauth_callback.html'

    def _build_context(self, request, status_value=None, error=None):
        pending = request.session.get('oauth_pending')
        provider = request.GET.get('provider')
        email = None
        display_name = None

        if pending:
            provider = pending.get('provider') or provider
            email = pending.get('email')

        if provider:
            display_name = provider.title()

        status_value = status_value or request.GET.get('status') or 'error'
        if status_value == 'pending' and not pending:
            status_value = 'error'
            error = error or 'No pending OAuth request'

        return {
            'status': status_value,
            'provider': provider,
            'display_name': display_name,
            'email': email,
            'error': error,
        }

    def get(self, request, *args, **kwargs):
        context = self._build_context(request)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            context = self._build_context(
                request,
                status_value='pending',
                error='Password confirmation does not match',
            )
            return render(request, self.template_name, context)

        from api.views.api import OAuthCreateUserView

        try:
            OAuthCreateUserView()._create_oauth_user(request, username, password)
        except ValidationError as exc:
            error_text = exc.detail
            if isinstance(error_text, (list, tuple)):
                error_text = error_text[0]
            context = self._build_context(request, status_value='pending', error=error_text)
            return render(request, self.template_name, context)

        return redirect('/account-setting')


class UpdateAccount(View):
    fail_template_name = 'user/account_update_fail.html'
    success_template_name = 'user/account_update_done.html'

    def get(self, request, uidb64, token, *args, **kwargs):
        user = get_object_or_404(User, pk=force_str(urlsafe_base64_decode(uidb64)))
        if user is not None and token_generator.check_token(user, token):
            cache_key = "user:serializer:%s" % user.pk
            from django.core.cache import cache
            data = cache.get(cache_key, None)
            if data:
                user_serializer = serializers.UserSerializer(
                    data=data, instance=user, partial=True
                )
                if user_serializer.is_valid():
                    user_serializer.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    cache.delete(cache_key)
                    return render(request, template_name=self.success_template_name)
        return render(request, template_name=self.fail_template_name)


class LoginDoneView(TemplateView):
    template_name = 'user/login_done.html'


class UserPasswordResetView(views.PasswordResetView):
    email_template_name = 'user/password_reset_email.html'
    success_url = reverse_lazy('user_password_reset_done')
    template_name = 'user/password_reset_form.html'


class UserPasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'


class UserPasswordResetConfirmView(views.PasswordResetConfirmView):
    success_url = reverse_lazy('user_password_reset_complete')
    template_name = 'user/password_reset_confirm.html'


class UserPasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'user/password_reset_complete.html'


class UserLogoutView(views.LogoutView):
    template_name = 'user/logout.html'
