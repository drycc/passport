from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from social_django.models import UserSocialAuth
from rest_framework.exceptions import ValidationError

from api.models import Message
from api.utils import (
    get_local_host,
    get_oauth_callback,
    get_user_socials,
    send_activation_email,
    send_email_notification,
    send_webhook_notification,
    timestamp2datetime,
    validate_reserved_names,
)

User = get_user_model()


class UtilsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='util-user',
            email='util@example.com',
            password='password123',
        )
        self.message = Message.objects.create(
            user=self.user,
            category='security',
            title='Utility message',
            content='Utility content',
            full_content='Utility content full',
            severity='warning',
        )

    def test_timestamp2datetime(self):
        dt = timestamp2datetime(0)
        self.assertEqual(dt.year, 1970)

    def test_get_local_host(self):
        request = self.factory.get('/user/info', secure=True, HTTP_HOST='example.com')
        self.assertEqual(get_local_host(request), 'https://example.com')

    @override_settings(SOCIAL_AUTH_LOGIN_CALLBACK_URL='/oauth/callback')
    def test_get_oauth_callback(self):
        request = self.factory.get('/user/login', secure=True, HTTP_HOST='example.com')
        callback = get_oauth_callback(request, 'linked', 'feishu')
        self.assertEqual(
            callback,
            'https://example.com/oauth/callback?status=linked&provider=feishu'
        )

    @override_settings(RESERVED_NAME_PATTERNS=[r'^admin$', r'^root$'])
    def test_validate_reserved_names_rejects_reserved(self):
        with self.assertRaises(ValidationError):
            validate_reserved_names('admin')

    @override_settings(RESERVED_NAME_PATTERNS=[r'^admin$', r'^root$'])
    def test_validate_reserved_names_accepts_normal_name(self):
        validate_reserved_names('normal-user')

    @override_settings(EMAIL_HOST='smtp.example.com')
    @patch('api.utils.render_to_string', return_value='rendered body')
    def test_send_activation_email(self, mock_render):
        request = self.factory.get('/user/registration', secure=True, HTTP_HOST='example.com')
        with patch.object(self.user, 'email_user') as mock_email_user:
            send_activation_email(request, self.user)

        mock_render.assert_called_once()
        mock_email_user.assert_called_once()

    @override_settings(EMAIL_HOST='smtp.example.com')
    @patch('api.utils.render_to_string', return_value='<b>Hello</b>')
    def test_send_email_notification(self, mock_render):
        with patch.object(self.user, 'email_user') as mock_email_user:
            send_email_notification(self.message)

        mock_render.assert_called_once()
        mock_email_user.assert_called_once()

    @patch('api.utils.requests.post')
    def test_send_webhook_notification(self, mock_post):
        mock_post.return_value.raise_for_status = Mock()

        send_webhook_notification(self.message, 'https://example.com/webhook')

        mock_post.assert_called_once()

    @patch('api.apps_extra.social_core.backends.__all__', new=[])
    def test_get_user_socials_without_backend_metadata(self):
        UserSocialAuth.objects.create(
            user=self.user,
            provider='feishu',
            uid='uid-1',
            extra_data={'email': 'social@example.com'},
        )

        results = get_user_socials(self.user)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['email'], 'social@example.com')
