"""
Test cases for API views
"""
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from oauth2_provider.models import AccessToken

from api.views import (
    ReadinessCheckView, LivenessCheckView, ActivateAccount
)
from api.forms import RegistrationForm

User = get_user_model()


class TestReadinessCheckView(TestCase):
    """Test readiness check view"""

    def test_readiness_check_get(self):
        request = RequestFactory().get('/readiness/')
        response = ReadinessCheckView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')

    def test_readiness_check_head(self):
        request = RequestFactory().head('/readiness/')
        response = ReadinessCheckView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestLivenessCheckView(TestCase):
    """Test liveness check view"""

    def test_liveness_check_get(self):
        request = RequestFactory().get('/liveness/')
        response = LivenessCheckView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')

    def test_liveness_check_head(self):
        request = RequestFactory().head('/liveness/')
        response = LivenessCheckView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestRegistrationView(TestCase):
    """Test registration view"""

    def setUp(self):
        self.factory = RequestFactory()

    def test_registration_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestActivateAccount(TestCase):
    """Test account activation view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_active=False
        )
        self.factory = RequestFactory()

    def test_activate_account_invalid_token(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.messages.storage.fallback import FallbackStorage

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        request = self.factory.get(f'/activate/{uid}/invalid-token/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = ActivateAccount.as_view()(request, uidb64=uid, token='invalid-token')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/activate/fail/')


class TestUserDetailView(APITestCase):
    """Test user detail viewset"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_user_detail(self):
        url = '/user/info'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class TestUserTokensView(APITestCase):
    """Test user tokens viewset"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.token = AccessToken.objects.create(
            user=self.user,
            token='tokentest',
            application=None,
            expires='9999-01-01T00:00:00Z',
            scope='read write'
        )

    def test_list_user_tokens(self):
        url = reverse('user_tokens')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_token(self):
        url = reverse('user_grants', args=[self.token.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AccessToken.objects.filter(id=self.token.id).exists())


class TestUserAccountPasswordView(APITestCase):
    """Test user account password view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpassword123'
        )
        self.client.force_authenticate(user=self.user)

    def test_update_password_valid(self):
        url = '/user/password'
        data = {
            'password': 'oldpassword123',
            'new_password': 'newpassword123'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
