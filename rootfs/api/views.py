import logging
import hashlib
import secrets
from django.conf import settings
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth import views
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from oauth2_provider.models import AccessToken

from api import serializers
from api.forms import AuthenticationForm, RegistrationForm
from api.exceptions import ServiceUnavailable, DryccException
from api.utils import (
    token_generator, get_local_host, send_activation_email, send_organization_invitation
)
from api.viewset import NormalUserViewSet
from api.models import Organization, OrganizationMember, OrganizationInvitation

User = get_user_model()
logger = logging.getLogger(__name__)


def is_organization_member(user, organization, role=None):
    kwargs = {'user': user, 'organization': organization}
    if role:
        kwargs['role'] = role
    return OrganizationMember.objects.filter(**kwargs).exists()


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


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('user_registration_done')

    def get(self, request, *args, **kwargs):
        if settings.LDAP_ENDPOINT or not settings.REGISTRATION_ENABLED:
            return render(request, template_name='user/registration_disable.html')
        return super().get(self, request, *args, **kwargs)

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
                messages.success(request, (
                    'Please Confirm your email to complete registration.'))
            else:
                user.is_active = True
                user.save()
            return self.form_valid(form)
        else:
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
        if user is not None and token_generator.check_token(
                user, token):
            user.is_active = True
            user.save()
            OrganizationInvitation.bulk_accept_by_email(user.email)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
    form_class = AuthenticationForm
    extra_context = {
        "registration_enabled": settings.REGISTRATION_ENABLED,
        "password_reset_enabled": True if settings.EMAIL_HOST else False,
    }
    template_name = 'user/login.html'


class UserDetailView(NormalUserViewSet):
    serializer_class = serializers.UserSerializer
    required_scopes = ['openid']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user_serializer = self.serializer_class(
            data=request.data,
            instance=request.user,
            partial=True
        )
        if user_serializer.is_valid():
            if settings.EMAIL_HOST:
                user = self.get_object()
                mail_subject = 'Update your account.'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                message = render_to_string(
                    'user/account_update_email.html', {
                        'uid': uid,
                        'user': user,
                        'token': token,
                        'domain': get_local_host(request)
                    })
                cache_key = "user:serializer:%s" % user.pk
                cache.set(cache_key, request.data, 60 * 30)
                user.email_user(mail_subject, message, fail_silently=True)
            else:
                user = user_serializer.save()
                OrganizationInvitation.bulk_accept_by_email(user.email)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        user = get_object_or_404(User, pk=force_str(urlsafe_base64_decode(uidb64)))
        if user is not None and token_generator.check_token(user, token):
            cache_key = "user:serializer:%s" % user.pk
            data = cache.get(cache_key, None)
            if data:
                user_serializer = serializers.UserSerializer(
                    data=data, instance=user, partial=True)
                if user_serializer.is_valid():
                    user_serializer.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    cache.delete(cache_key)
                    return render(request, template_name='user/account_update_done.html')
        return render(request, template_name='user/account_update_fail.html')


class UserAvatarViewSet(NormalUserViewSet):

    @method_decorator(cache_page(60 * 5))
    def avatar(self, request, *args, **kwargs):
        user = User.objects.filter(username=kwargs["username"]).first()
        size = request.GET.get("s", "80")
        md5 = hashlib.md5()
        if user:
            md5.update(user.email.encode("utf8"))
        return HttpResponseRedirect(settings.AVATAR_URL + md5.hexdigest() + "?s=" + size)


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


class UserTokensView(ListViewSet):
    model = AccessToken
    serializer_class = serializers.UserTokensSerializer
    order_by = '-created'

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


class OrganizationViewSet(ModelViewSet):
    """
    ViewSet for Organization model.
    """
    serializer_class = serializers.OrganizationSerializer
    lookup_field = 'name'

    def get_queryset(self):
        return Organization.objects.filter(
            organizationmember__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        organization = serializer.save()
        OrganizationMember.objects.create(
            user=self.request.user, organization=organization, role='admin'
        )

    def get_object(self):
        """Override to get organization by name instead of pk"""
        return get_object_or_404(Organization, name=self.kwargs['name'])

    def partial_update(self, request, *args, **kwargs):
        """Only admins can update organizations"""
        organization = self.get_object()
        if not is_organization_member(request.user, organization, role='admin'):
            return Response(
                {"detail": "Only organization admins can update organizations"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Only admins can delete organizations"""
        organization = self.get_object()
        if not is_organization_member(request.user, organization, role='admin'):
            return Response(
                {"detail": "Only organization admins can delete organizations"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class OrganizationMemberViewSet(ModelViewSet):
    """
    ViewSet for OrganizationMember model.
    """
    serializer_class = serializers.OrganizationMemberSerializer

    def get_queryset(self):
        organization = get_object_or_404(Organization, name=self.kwargs['name'])
        # Check if user has access to this organization
        if is_organization_member(self.request.user, organization):
            return OrganizationMember.objects.filter(organization=organization)
        return OrganizationMember.objects.none()

    def get_object(self):
        """Override to get member by username and organization name"""
        organization = get_object_or_404(Organization, name=self.kwargs['name'])
        return get_object_or_404(
            OrganizationMember, organization=organization, user__username=self.kwargs['user']
        )

    def partial_update(self, request, *args, **kwargs):
        """Update a member. Admins can update any member (role and alerts).
        Non-admins can only update their own alerts field."""
        member = self.get_object()
        is_admin = is_organization_member(request.user, member.organization, role='admin')

        # Check if organization has only one member
        member_count = OrganizationMember.objects.filter(
            organization=member.organization
        ).count()
        is_only_member = member_count == 1

        # Only member cannot modify role
        if is_only_member and 'role' in request.data:
            return Response(
                {"detail": "Cannot modify role: organization only has one member"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Non-admin users restrictions
        if not is_admin:
            # Cannot update other members
            if request.user != member.user:
                return Response(
                    {"detail": "Only organization admins can update other members"},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Cannot modify own role
            if 'role' in request.data:
                return Response(
                    {"detail": "Cannot modify your own role"},
                    status=status.HTTP_403_FORBIDDEN
                )

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete a member. Admins can delete any member.
        Non-admins can only delete themselves (leave organization)."""
        member = self.get_object()
        is_admin = is_organization_member(request.user, member.organization, role='admin')

        # Check if organization has only one member
        member_count = OrganizationMember.objects.filter(
            organization=member.organization
        ).count()
        is_only_member = member_count == 1

        # Only member cannot delete self
        if is_only_member and request.user == member.user:
            return Response(
                {"detail": "Cannot delete: organization only has one member"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Non-admin can delete self
        if request.user == member.user:
            return super().destroy(request, *args, **kwargs)

        # Admin can delete any member
        if is_admin:
            return super().destroy(request, *args, **kwargs)

        # Other cases forbidden
        return Response(
            {"detail": "Only organization admins can remove other members"},
            status=status.HTTP_403_FORBIDDEN
        )


class OrganizationInvitationViewSet(ModelViewSet):
    """
    ViewSet for OrganizationInvitation model.
    """
    serializer_class = serializers.OrganizationInvitationSerializer

    def get_queryset(self):
        organization = get_object_or_404(Organization, name=self.kwargs['name'])
        if is_organization_member(self.request.user, organization):
            return OrganizationInvitation.objects.filter(
                organization=organization, accepted=False)
        return OrganizationInvitation.objects.none()

    def get_object(self):
        """Override to get invitation by uid and organization name"""
        return get_object_or_404(
            OrganizationInvitation,
            organization=get_object_or_404(Organization, name=self.kwargs['name']),
            token=self.kwargs['uid'],
            accepted=False,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.accept()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Check if user has permission to create invitations for this organization
        organization = get_object_or_404(Organization, name=self.kwargs['name'])
        if not is_organization_member(self.request.user, organization, role='admin'):
            raise ValidationError("Only organization admins can create invitations")
        # Throw an error if the user is already a member
        user = User.objects.filter(email=serializer.validated_data['email']).first()
        if user and is_organization_member(user, organization):
            raise ValidationError("User is already a member of the organization")
        # Generate token and set inviter
        token = secrets.token_hex(64)
        try:
            invitation = serializer.save(
                token=token, inviter=self.request.user, organization=organization)
            if settings.EMAIL_HOST:
                send_organization_invitation(self.request, invitation)
            else:
                invitation.accept()
        except IntegrityError:
            raise ValidationError("User already has pending invitation")
        except User.DoesNotExist:
            raise ValidationError("No user with this email exists.")

    def destroy(self, request, *args, **kwargs):
        """Only admins can revoke invitations"""
        invitation = self.get_object()
        if not is_organization_member(request.user, invitation.organization, role='admin'):
            return Response(
                {"detail": "Only organization admins can revoke invitations"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
