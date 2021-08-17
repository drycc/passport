"""
Classes to serialize the RESTful representation of Drycc API models.
"""
import logging

from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from oauth2_provider.models import Grant, AccessToken
from oauth2_provider.oauth2_validators import OAuth2Validator
from rest_framework import serializers

from api.exceptions import DryccException
from api.utils import timestamp2datetime

logger = logging.getLogger(__name__)


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=False)
    email = serializers.CharField(max_length=254, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', "first_name", "last_name",
                  "is_staff", "is_active", "is_superuser")

    def update(self, instance, validated_data):
        if settings.LDAP_ENDPOINT:
            raise DryccException(
                "You cannot change user info when ldap is enabled.")
        if validated_data.get('username'):
            qs = User.objects.filter(username=validated_data.get('username')).\
                exclude(username=instance.username)
            if qs:
                raise DryccException("new username already exists.")
            instance.username = validated_data.get('username')
        if validated_data.get('email'):
            instance.email = validated_data.get('email')
        instance.save()
        return instance


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ListSerializer(serializers.Serializer):
    section = serializers.CharField(max_length=500, required=False)

    @staticmethod
    def validate_section(section):
        field = section.split(',') if section else None
        if field is None:
            return None
        return [timestamp2datetime(float(field[0])),
                timestamp2datetime(float(field[1]))]


class UserGrantsSerializer(serializers.ModelSerializer):
    """Serialize user status for a Grant model."""

    class Meta:
        model = Grant
        fields = '__all__'
        read_only_fields = ['id', 'user', 'code', 'application', 'expires',
                            'redirect_uri', 'scope', 'created', 'updated',
                            'code_challenge', 'code_challenge_method', 'nonce',
                            'claims']


class UserTokensSerializer(serializers.ModelSerializer):
    """Serialize user status for a AccessToken model."""
    application = serializers.ReadOnlyField(source='application.name')

    class Meta:
        model = AccessToken
        fields = '__all__'
        read_only_fields = ['id', 'user', 'source_refresh_token', 'token',
                            'id_token', 'application', 'expires', 'scope',
                            'created', 'updated']


class UserLogsSerializer(serializers.ModelSerializer):
    """Serialize user status for a AccessToken model."""

    class Meta:
        model = LogEntry
        fields = '__all__'
        read_only_fields = ['action_time', 'user', 'content_type', 'object_id',
                            'object_repr', 'action_flag', 'change_message']


class CustomOAuth2Validator(OAuth2Validator):

    def get_additional_claims(self, request):
        claims = super().get_additional_claims(request)
        claims["id"] = request.user.id
        claims["name"] = request.user.username
        claims["username"] = request.user.username
        claims["email"] = request.user.email
        claims["first_name"] = request.user.first_name
        claims["last_name"] = request.user.last_name
        claims["is_staff"] = request.user.is_staff
        claims["is_active"] = request.user.is_active
        claims["is_superuser"] = request.user.is_superuser
        return claims
