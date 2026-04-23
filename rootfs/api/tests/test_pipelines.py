from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from social_django.models import UserSocialAuth

from api.apps_extra.social_core.pipelines import (
    handle_authenticated_binding, require_username_password
)

User = get_user_model()


class PipelineTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='pipe-user',
            email='pipe@example.com',
            password='password123',
        )

    def _make_backend(self, request, name='feishu'):
        strategy = Mock()
        strategy.request = request
        strategy.session_set = Mock()
        backend = Mock()
        backend.name = name
        backend.strategy = strategy
        return backend

    @patch(
        'api.apps_extra.social_core.pipelines.get_oauth_callback',
        return_value='/oauth/callback?status=linked'
    )
    def test_handle_authenticated_binding_creates_identity(self, _mock_callback):
        request = self.factory.get('/oauth/callback')
        request.user = self.user
        backend = self._make_backend(request)

        response = handle_authenticated_binding(
            backend, 'uid-1', {}, {'email': 'pipe@example.com'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserSocialAuth.objects.filter(
            user=self.user, provider='feishu', uid='uid-1'
        ).exists())

    @patch(
        'api.apps_extra.social_core.pipelines.get_oauth_callback',
        return_value='/oauth/callback?status=conflict'
    )
    def test_handle_authenticated_binding_conflict(self, _mock_callback):
        other = User.objects.create_user(
            username='other', email='other@example.com', password='password123'
        )
        UserSocialAuth.objects.create(
            user=other, provider='feishu', uid='uid-1', extra_data={}
        )
        request = self.factory.get('/oauth/callback')
        request.user = self.user
        backend = self._make_backend(request)

        response = handle_authenticated_binding(
            backend, 'uid-1', {}, {'email': 'pipe@example.com'}
        )

        self.assertEqual(response.status_code, 302)

    @patch(
        'api.apps_extra.social_core.pipelines.get_oauth_callback',
        return_value='/oauth/callback?status=already_linked'
    )
    def test_handle_authenticated_binding_already_linked(self, _mock_callback):
        UserSocialAuth.objects.create(
            user=self.user, provider='feishu', uid='uid-1', extra_data={}
        )
        request = self.factory.get('/oauth/callback')
        request.user = self.user
        backend = self._make_backend(request)

        response = handle_authenticated_binding(
            backend, 'uid-1', {}, {'email': 'pipe@example.com'}
        )

        self.assertEqual(response.status_code, 302)

    @patch(
        'api.apps_extra.social_core.pipelines.get_oauth_callback',
        return_value='/oauth/callback?status=pending'
    )
    def test_require_username_password_sets_pending_session(self, _mock_callback):
        request = self.factory.get('/oauth/callback')
        request.user = Mock(is_authenticated=False)
        backend = self._make_backend(request)

        response = require_username_password(
            backend, 'uid-1', {'email': 'pipe@example.com'},
            {'email': 'pipe@example.com'}
        )

        self.assertEqual(response.status_code, 302)
        backend.strategy.session_set.assert_called_once()

    @patch(
        'api.apps_extra.social_core.pipelines.get_oauth_callback',
        return_value='/oauth/callback?status=missing_email'
    )
    def test_require_username_password_requires_email(self, _mock_callback):
        request = self.factory.get('/oauth/callback')
        request.user = Mock(is_authenticated=False)
        backend = self._make_backend(request)

        response = require_username_password(backend, 'uid-1', {}, {})

        self.assertEqual(response.status_code, 302)
