"""
Test cases for API views
"""
from unittest.mock import patch

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from oauth2_provider.models import AccessToken
from social_django.models import UserSocialAuth
from django.core.cache import cache

from api.views import (
    ReadinessCheckView, LivenessCheckView, ActivateAccount
)
from api.forms import RegistrationForm
from api.models import Message, MessagePreference

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

    @patch('api.views.web.settings.REGISTRATION_ENABLED', False)
    def test_registration_get_disabled(self):
        response = self.client.get(reverse('registration'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'The registration function of drycc passport is not enabled.',
            status_code=200,
        )

    @patch('api.views.web.settings.REGISTRATION_ENABLED', True)
    @patch('api.views.web.settings.EMAIL_HOST', '')
    def test_registration_post_creates_active_user_when_email_disabled(self):
        response = self.client.post(reverse('registration'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'h-captcha-response': 'PASSED',
        })

        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newuser')
        self.assertTrue(user.is_active)

    @patch('api.views.web.settings.REGISTRATION_ENABLED', True)
    @patch('api.views.web.settings.EMAIL_HOST', 'smtp.example.com')
    @patch('api.views.web.send_activation_email')
    def test_registration_post_sends_activation_email_when_email_enabled(
        self, mock_send_activation_email
    ):
        response = self.client.post(reverse('registration'), {
            'username': 'inactiveuser',
            'email': 'inactive@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'h-captcha-response': 'PASSED',
        })

        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='inactiveuser')
        self.assertFalse(user.is_active)
        mock_send_activation_email.assert_called_once()


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

    def test_activate_account_valid_token(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.messages.storage.fallback import FallbackStorage
        from api.utils import token_generator

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = token_generator.make_token(self.user)
        request = self.factory.get(f'/activate/{uid}/{token}/')
        request.session = self.client.session
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = ActivateAccount.as_view()(request, uidb64=uid, token=token)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/activate/done/')
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)


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

    @patch('api.views.api.settings.EMAIL_HOST', 'smtp.example.com')
    @patch('api.views.api.render_to_string', return_value='mail-body')
    def test_update_user_detail_sends_confirmation_email_and_caches_data(self, _mock_render):
        url = '/user/info'
        response = self.client.put(url, {'first_name': 'Updated'})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, '')
        self.assertEqual(cache.get(f'user:serializer:{self.user.pk}'), {'first_name': 'Updated'})

    def test_update_user_detail_fails_validation(self):
        url = '/user/info'
        response = self.client.put(url, {'email': 'invalid-email'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


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


class TestIdentityProviderView(APITestCase):

    @patch('api.views.api.settings.SOCIAL_AUTH_FEISHU_KEY', 'key')
    @patch('api.views.api.settings.SOCIAL_AUTH_FEISHU_SECRET', 'secret')
    @patch('api.views.api.settings.SOCIAL_AUTH_GOOGLE_KEY', '')
    @patch('api.views.api.settings.SOCIAL_AUTH_GOOGLE_SECRET', '')
    def test_only_configured_identity_providers_are_returned(self):
        response = self.client.get(reverse('user_identity_providers'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        provider_names = [item['name'] for item in response.data['results']]
        self.assertIn('feishu', provider_names)
        self.assertNotIn('google', provider_names)


class TestUserIdentityView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='identity-user',
            email='identity@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='other-user',
            email='other@example.com',
            password='testpass123'
        )
        self.identity = UserSocialAuth.objects.create(
            user=self.user,
            provider='feishu',
            uid='uid-1',
            extra_data={'email': 'identity@example.com'}
        )
        self.other_identity = UserSocialAuth.objects.create(
            user=self.other_user,
            provider='github',
            uid='uid-2',
            extra_data={'email': 'other@example.com'}
        )
        self.client.force_authenticate(user=self.user)

    def test_list_user_identities(self):
        response = self.client.get(reverse('user_identities-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['provider'], 'feishu')

    def test_delete_own_identity(self):
        response = self.client.delete(reverse('user_identities-detail', args=[self.identity.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserSocialAuth.objects.filter(id=self.identity.id).exists())

    def test_cannot_delete_other_user_identity(self):
        response = self.client.delete(
            reverse('user_identities-detail', args=[self.other_identity.id])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestOAuthPendingAndCreateView(APITestCase):

    def setUp(self):
        self.client_handler = self.client.handler

    def test_oauth_pending_without_session_data(self):
        response = self.client.get(reverse('user_oauth_pending'))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_oauth_pending_with_session_data(self):
        session = self.client.session
        session['oauth_pending'] = {
            'provider': 'feishu',
            'email': 'pending@example.com',
            'uid': 'pending-uid',
            'extra_data': {'email': 'pending@example.com'},
        }
        session.save()

        response = self.client.get(reverse('user_oauth_pending'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['provider'], 'feishu')
        self.assertEqual(response.data['email'], 'pending@example.com')

    def test_oauth_create_user_success(self):
        session = self.client.session
        session['oauth_pending'] = {
            'provider': 'feishu',
            'email': 'new@example.com',
            'uid': 'pending-uid',
            'extra_data': {'email': 'new@example.com'},
        }
        session.save()

        response = self.client.post(reverse('user_oauth_create'), {
            'username': 'oauth-user',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(username='oauth-user', email='new@example.com').exists()
        )
        self.assertTrue(
            UserSocialAuth.objects.filter(provider='feishu', uid='pending-uid').exists()
        )

    def test_oauth_create_user_requires_pending(self):
        response = self.client.post(reverse('user_oauth_create'), {
            'username': 'oauth-user',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_oauth_create_user_requires_username(self):
        session = self.client.session
        session['oauth_pending'] = {
            'provider': 'feishu',
            'email': 'new@example.com',
            'uid': 'pending-uid',
            'extra_data': {'email': 'new@example.com'},
        }
        session.save()

        response = self.client.post(reverse('user_oauth_create'), {
            'password': 'password123',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_oauth_create_user_rejects_existing_email(self):
        User.objects.create_user(
            username='exists', email='new@example.com', password='password123'
        )
        session = self.client.session
        session['oauth_pending'] = {
            'provider': 'feishu',
            'email': 'new@example.com',
            'uid': 'pending-uid',
            'extra_data': {'email': 'new@example.com'},
        }
        session.save()

        response = self.client.post(reverse('user_oauth_create'), {
            'username': 'oauth-user',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_oauth_create_user_rejects_existing_identity(self):
        existing_user = User.objects.create_user(
            username='exists', email='exists@example.com', password='password123'
        )
        UserSocialAuth.objects.create(
            user=existing_user,
            provider='feishu',
            uid='pending-uid',
            extra_data={'email': 'exists@example.com'}
        )
        session = self.client.session
        session['oauth_pending'] = {
            'provider': 'feishu',
            'email': 'new@example.com',
            'uid': 'pending-uid',
            'extra_data': {'email': 'new@example.com'},
        }
        session.save()

        response = self.client.post(reverse('user_oauth_create'), {
            'username': 'oauth-user',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserMessageViews(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='message-user',
            email='message@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='other-message-user',
            email='other-message@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.message1 = Message.objects.create(
            user=self.user,
            category='system',
            title='System message',
            content='System content',
            severity='info'
        )
        self.message2 = Message.objects.create(
            user=self.user,
            category='security',
            title='Security message',
            content='Security content',
            severity='warning'
        )
        self.other_message = Message.objects.create(
            user=self.other_user,
            category='system',
            title='Other message',
            content='Other content',
            severity='info'
        )

    def test_list_messages(self):
        response = self.client.get(reverse('user_messages-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('results', response.data)

    def test_filter_messages_by_category(self):
        response = self.client.get(reverse('user_messages-list'), {'category': 'security'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['category'], 'security')

    def test_list_messages_supports_limit_offset_pagination(self):
        response = self.client.get(reverse('user_messages-list'), {'limit': 1, 'offset': 0})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['count'], 2)

    def test_create_message_for_current_user(self):
        response = self.client.post(reverse('user_messages-list'), {
            'category': 'alert',
            'title': 'Created from API',
            'content': 'API created content',
            'full_content': 'API created full content',
            'severity': 'warning',
            'is_read': False,
            'action_link': '/messages',
            'action_text': 'Open',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Message.objects.get(id=response.data['id'])
        self.assertEqual(created.user, self.user)
        self.assertEqual(created.category, 'alert')

    def test_mark_all_messages_as_read(self):
        response = self.client.put(reverse('user_messages-mark-all-read'))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Message.objects.filter(user=self.user, is_read=False).exists())

    def test_get_message_detail_marks_message_as_read(self):
        response = self.client.get(reverse('user_messages-detail', args=[self.message1.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message1.refresh_from_db()
        self.assertTrue(self.message1.is_read)

    def test_cannot_get_other_users_message(self):
        response = self.client.get(reverse('user_messages-detail', args=[self.other_message.id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestUserMessagePreferenceView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='preference-user',
            email='preference@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_creates_preference_if_missing(self):
        response = self.client.get(reverse('user_message_preferences'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(MessagePreference.objects.filter(user=self.user).exists())

    def test_put_updates_preference(self):
        response = self.client.put(reverse('user_message_preferences'), {
            'email_alerts': False,
            'notify_alert': False,
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        preference = MessagePreference.objects.get(user=self.user)
        self.assertFalse(preference.email_alerts)
        self.assertFalse(preference.notify_alert)


class TestUserLoginIdentityLinking(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='login-user',
            email='login@example.com',
            password='password123'
        )

    def test_login_links_pending_identity(self):
        session = self.client.session
        session['oauth_pending'] = {
            'provider': 'feishu',
            'uid': 'uid-100',
            'extra_data': {'email': 'login@example.com'},
        }
        session.save()

        response = self.client.post(reverse('user_login') + '?identity_linking=1', {
            'username': 'login-user',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn('status=linked', response.url)
        self.assertTrue(UserSocialAuth.objects.filter(
            user=self.user, provider='feishu', uid='uid-100'
        ).exists())

    def test_login_identity_linking_conflict_redirects(self):
        other_user = User.objects.create_user(
            username='other-login-user',
            email='other-login@example.com',
            password='password123'
        )
        UserSocialAuth.objects.create(
            user=other_user,
            provider='feishu',
            uid='uid-100',
            extra_data={'email': 'other-login@example.com'}
        )
        session = self.client.session
        session['oauth_pending'] = {
            'provider': 'feishu',
            'uid': 'uid-100',
            'extra_data': {'email': 'login@example.com'},
        }
        session.save()

        response = self.client.post(reverse('user_login') + '?identity_linking=1', {
            'username': 'login-user',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn('status=conflict', response.url)

    @patch('api.views.web.settings.EMAIL_HOST', 'smtp.example.com')
    @patch('api.views.web.settings.REGISTRATION_ENABLED', True)
    def test_login_page_context_shows_identity_linking_error(self):
        response = self.client.post(reverse('user_login') + '?identity_linking=1', {
            'username': 'login-user',
            'password': 'wrong-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Identity linking login failed. Please try again.')

    @patch('api.views.web.settings.EMAIL_HOST', '')
    @patch('api.views.web.settings.REGISTRATION_ENABLED', False)
    def test_login_page_context_flags_follow_settings(self):
        response = self.client.get(reverse('user_login') + '?identity_linking=1')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Identity Linking')


class TestOAuthCallbackTemplateView(TestCase):

    def test_get_without_pending_renders_error_state(self):
        response = self.client.get(reverse('oauth_callback') + '?status=pending')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OAuth flow error. Please try again.')

    @patch('api.views.api.OAuthCreateUserView._create_oauth_user')
    def test_post_password_mismatch_renders_error(self, _mock_create):
        session = self.client.session
        session['oauth_pending'] = {
            'provider': 'feishu',
            'email': 'pending@example.com',
        }
        session.save()

        response = self.client.post(reverse('oauth_callback'), {
            'username': 'oauth-user',
            'password': 'password123',
            'confirm_password': 'different123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password confirmation does not match')

    @patch('api.views.api.OAuthCreateUserView._create_oauth_user')
    def test_post_success_redirects_account_setting(self, mock_create):
        session = self.client.session
        session['oauth_pending'] = {
            'provider': 'feishu',
            'email': 'pending@example.com',
        }
        session.save()

        response = self.client.post(reverse('oauth_callback'), {
            'username': 'oauth-user',
            'password': 'password123',
            'confirm_password': 'password123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account-setting')
        mock_create.assert_called_once()


class TestUpdateAccountView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='update-user',
            email='update@example.com',
            password='password123'
        )

    def test_update_account_applies_cached_serializer_data(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from api.utils import token_generator

        cache.set(f'user:serializer:{self.user.pk}', {'first_name': 'Cached'}, 1800)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = token_generator.make_token(self.user)

        response = self.client.get(reverse('user_update_account', args=[uid, token]))

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Cached')
        self.assertIsNone(cache.get(f'user:serializer:{self.user.pk}'))

    def test_update_account_invalid_token_renders_fail(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        response = self.client.get(reverse('user_update_account', args=[uid, 'invalid-token']))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'update fail', status_code=200)

    def test_update_account_without_cached_data_renders_fail(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from api.utils import token_generator

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = token_generator.make_token(self.user)
        response = self.client.get(reverse('user_update_account', args=[uid, token]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'update fail', status_code=200)


class TestPasswordResetViews(TestCase):

    def test_password_reset_form_page_loads(self):
        response = self.client.get(reverse('user_password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_page_loads(self):
        response = self.client.get(reverse('user_password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_page_loads(self):
        response = self.client.get(reverse('user_password_reset_complete'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_confirm_invalid_token_page_loads(self):
        response = self.client.get(
            reverse('user_password_reset_confirm', args=['invalid', 'invalid-token'])
        )
        self.assertEqual(response.status_code, 200)
