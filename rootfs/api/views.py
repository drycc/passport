import logging

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import views
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api import serializers
from api.exceptions import ServiceUnavailable, DryccException
from api.serializers import RegisterForm
from api.utils import account_activation_token, get_local_host
from api.viewset import NormalUserViewSet

logger = logging.getLogger(__name__)


class ReadinessCheckView(View):
    """
    Simple readiness check view to determine DB connection / query.
    """

    def get(self, request):
        try:
            import django.db
            with django.db.connection.cursor() as c:
                c.execute("SELECT 0")
        except django.db.Error as e:
            raise ServiceUnavailable("Database health check failed") from e

        return HttpResponse("OK")

    head = get


class LivenessCheckView(View):
    """
    Simple liveness check view to determine if the server
    is responding to HTTP requests.
    """

    def get(self, request):
        return HttpResponse("OK")

    head = get


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('register_done')

    def get(self, request, *args, **kwargs):
        if settings.LDAP_ENDPOINT or not settings.REGISTER_ENABLED:
            return render(request, template_name='user/register_fail.html')
        return CreateView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if settings.LDAP_ENDPOINT or not settings.REGISTER_ENABLED:
            return render(request, template_name='user/register_fail.html')
        form = self.form_class(request.POST)
        self.object = None
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_active = False
            user.save()
            domain = get_local_host(request)
            mail_subject = 'Activate your account.'
            message = render_to_string(
                'user/account_activation_email.html', {
                    'user': user,
                    'domain': domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            user.email_user(mail_subject, message)
            messages.success(request, (
                'Please Confirm your email to complete registration.'))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class RegisterDoneView(TemplateView):
    template_name = 'user/register_done.html'
    title = _('Activate email sent')


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(
                user, token):
            user.is_active = True
            user.is_staff = True
            user.save()
            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Your account have been confirmed.')
            return redirect('/user/activate/done/')
        else:
            messages.warning(request, (
                'The confirmation link was invalid, possibly because it has already been used.'))  # noqa
            return redirect('/user/activate/fail/')


class ActivateAccountDoneView(TemplateView):
    template_name = 'user/account_activation_done.html'
    title = _('Activate account done')


class ActivateAccountFailView(TemplateView):
    template_name = 'user/account_activation_fail.html'
    title = _('Activate account fail')


class UserLoginView(views.LoginView):
    template_name = 'user/login.html'


class UserDetailView(NormalUserViewSet):
    serializer_class = serializers.UserSerializer
    required_scopes = ['openid']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = serializers.UserSerializer(data=request.data,
                                          instance=request.user,
                                          partial=True)
        if user.is_valid():
            user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserEmailView(NormalUserViewSet):
    serializer_class = serializers.UserEmailSerializer
    required_scopes = ['openid']

    def get_object(self):
        return self.request.user


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


class ListViewSet(ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        serializerlist = serializers.ListSerializer(
            data=self.request.query_params)
        serializerlist.is_valid(raise_exception=True)
        q = Q(user=self.request.user)
        if serializerlist.validated_data.get('section'):
            q &= Q(created__range=serializerlist.validated_data.get('section'))
        return self.model.objects.filter(
            q, **serializer.validated_data).order_by(self.order_by)[0:100]


class UserTokensTemplateView(ListViewSet):
    from oauth2_provider.models import AccessToken
    model = AccessToken
    serializer_class = serializers.UserTokensSerializer
    order_by = '-created'

    def retrieve(self, request, *args, **kwargs):
        tokens = self.get_queryset(*args, **kwargs)
        serializer = self.get_serializer(tokens, many=True)
        return Response(serializer.data)


class UserTokenDeleteView(ListViewSet):
    from oauth2_provider.models import AccessToken
    model = AccessToken

    def destroy(self, request, *args, **kwargs):
        token = get_object_or_404(self.model,
                                  id=self.kwargs['pk'],
                                  user=request.user)

        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAccountPasswordView(ListViewSet):

    def update(self, request, *args, **kwargs):
        if settings.LDAP_ENDPOINT:
            raise DryccException(
                "You cannot change user info when ldap is enabled.")
        if not request.data.get('new_password'):
            raise DryccException("new_password is a required field")
        if not request.data.get('password'):
            raise DryccException("password is a required field")
        if len(request.data.get('new_password')) < 8:
            raise DryccException("password must be 8 or more characters. ")
        if not request.user.check_password(request.data['password']):
            raise AuthenticationFailed('Current password does not match')
        request.user.set_password(request.data['new_password'])
        request.user.save()
        auth.logout(request)
        return HttpResponse(status=204)
