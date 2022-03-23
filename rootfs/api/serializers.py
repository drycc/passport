"""
Classes to serialize the RESTful representation of Drycc API models.
"""
import logging

from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from oauth2_provider.models import Grant, AccessToken
from rest_framework import serializers

from api.utils import timestamp2datetime

User = get_user_model()
logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_staff', 'is_active', 'is_superuser')
        read_only_fields = ('id', 'username', 'is_staff', 'is_active',
                            'is_superuser')


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
