from django.conf import settings
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse_lazy
from django.views.generic import View

from rest_framework import status, viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, DestroyModelMixin

from oauth2_provider.models import AccessToken
from social_django.models import UserSocialAuth

from api import serializers
from api.exceptions import ServiceUnavailable, DryccException
from api.models import Message, MessagePreference
from api.utils import get_local_host, get_user_socials, token_generator


User = get_user_model()


class NormalUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


class ReadinessCheckView(View):
    """Simple readiness check view to determine DB connection / query."""

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
    """Simple liveness check view to determine if the server is alive."""

    def get(self, request):
        return HttpResponse("OK")

    head = get


class IdentityProviderView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        from api.apps_extra.social_core import backends

        results = []
        for backend_cls in backends.__all__:
            key_setting = f'SOCIAL_AUTH_{backend_cls.name.upper()}_KEY'
            secret_setting = f'SOCIAL_AUTH_{backend_cls.name.upper()}_SECRET'
            if getattr(settings, key_setting, None) and getattr(settings, secret_setting, None):
                results.append({
                    'name': backend_cls.name,
                    'icon': backend_cls.icon,
                    'login_url': reverse_lazy('social:begin', args=(backend_cls.name,)),
                })

        return Response({'count': len(results), 'results': results})


class UserIdentityViewSet(NormalUserViewSet):
    serializer_class = serializers.UserEmailSerializer
    http_method_names = ['get', 'delete']

    def get_queryset(self):
        return UserSocialAuth.objects.filter(user=self.request.user).order_by('id')

    def list(self, request, *args, **kwargs):
        results = get_user_socials(request.user)
        return Response({'count': len(results), 'results': results})

    def destroy(self, request, *args, **kwargs):
        identity = self.get_object()
        identity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OAuthPendingView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        pending = request.session.get('oauth_pending')
        if not pending:
            return Response(
                {'detail': 'No pending OAuth request'}, status=status.HTTP_404_NOT_FOUND
            )

        from api.apps_extra.social_core import backends

        backend_map = {backend_cls.name: backend_cls for backend_cls in backends.__all__}
        backend_cls = backend_map.get(pending.get('provider'))
        return Response({
            'provider': pending.get('provider'),
            'email': pending.get('email'),
            'icon': backend_cls.icon if backend_cls else '',
            'display_name': pending.get('provider', '').title(),
        })


class UserMessageViewSet(NormalUserViewSet):
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.filter(user=self.request.user)
        category = self.request.query_params.get('category')
        if category and category != 'all':
            queryset = queryset.filter(category=category)
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        message = self.get_object()
        if not message.is_read:
            message.is_read = True
            message.save(update_fields=['is_read'])
        serializer = self.get_serializer(message)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], url_path='mark-all-read')
    def mark_all_read(self, request, *args, **kwargs):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OAuthCreateUserView(APIView):
    permission_classes = (AllowAny, )

    def _create_oauth_user(self, request, username, password):
        pending = request.session.get('oauth_pending')
        if not pending:
            raise ValidationError('No pending OAuth request')

        if not username:
            raise ValidationError('username is a required field')
        if not password:
            raise ValidationError('password is a required field')
        if len(password) < 8:
            raise ValidationError('password must be 8 or more characters')

        email = pending.get('email')
        if not email:
            raise ValidationError('email is missing from oauth provider')
        if User.objects.filter(email=email).exists():
            raise ValidationError('email is already registered')

        provider = pending.get('provider')
        uid = pending.get('uid')
        extra_data = pending.get('extra_data') or {}

        if not provider or not uid:
            request.session.pop('oauth_pending', None)
            raise ValidationError('invalid oauth pending data')

        existing = UserSocialAuth.objects.filter(provider=provider, uid=uid).first()
        if existing:
            request.session.pop('oauth_pending', None)
            raise ValidationError('identity is already linked to another account')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError:
            raise ValidationError('username is already taken')

        UserSocialAuth.objects.create(
            user=user,
            provider=provider,
            uid=uid,
            extra_data=extra_data,
        )

        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        request.session.pop('oauth_pending', None)
        return user

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        self._create_oauth_user(request, username, password)
        return Response({'status': 'created'}, status=status.HTTP_201_CREATED)


class UserDetailView(NormalUserViewSet):
    serializer_class = serializers.UserSerializer
    required_scopes = ['openid']
    email_template_name = 'user/account_update_email.html'

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user_serializer = self.serializer_class(
            data=request.data,
            instance=request.user,
            partial=True,
        )
        user_serializer.is_valid(raise_exception=True)
        if getattr(settings, 'EMAIL_HOST', ''):
            user = self.get_object()
            mail_subject = 'Update your account.'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            message = render_to_string(
                self.email_template_name,
                {
                    'uid': uid,
                    'user': user,
                    'token': token,
                    'domain': get_local_host(request),
                },
            )
            cache_key = "user:serializer:%s" % user.pk
            cache.set(cache_key, request.data, 60 * 30)
            user.email_user(mail_subject, message, fail_silently=True)
        else:
            user_serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserEmailView(NormalUserViewSet):
    serializer_class = serializers.UserEmailSerializer
    required_scopes = ['openid']

    def get_object(self):
        return self.request.user


class UserTokensView(ListModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = serializers.UserTokensSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AccessToken.objects.filter(user=self.request.user).order_by('-created')

    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=self.kwargs['pk'])


class UserAccountPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if settings.LDAP_ENDPOINT:
            raise DryccException("You cannot change user info when ldap is enabled.")
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

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserMessagePreferenceViewSet(NormalUserViewSet):
    serializer_class = serializers.MessagePreferenceSerializer
    http_method_names = ['get', 'put', 'patch']

    def get_object(self):
        preference, _ = MessagePreference.objects.get_or_create(user=self.request.user)
        return preference

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
