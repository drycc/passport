from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from api.models import Message, MessagePreference
from api.tasks import send_notification

User = get_user_model()


@override_settings(EMAIL_HOST='smtp.example.com')
class NotificationTaskTestCase(TestCase):
    def setUp(self):
        delay_patcher = patch('api.tasks.send_notification.delay')
        self.addCleanup(delay_patcher.stop)
        self.mock_delay = delay_patcher.start()

        self.user = User.objects.create_user(
            username='task-user',
            email='task@example.com',
            password='password123',
        )
        self.preference = MessagePreference.objects.create(
            user=self.user,
            email_alerts=True,
            push_alerts=True,
            webhook_url='https://example.com/webhook',
            notify_security=True,
            notify_system=True,
            notify_product=True,
            notify_alert=True,
            notify_service=True,
        )
        self.message = Message.objects.create(
            user=self.user,
            category='security',
            title='Security event',
            content='A security event occurred',
            full_content='A security event occurred in detail',
            severity='warning',
        )

    @patch('api.tasks.send_email_notification')
    @patch('api.tasks.send_webhook_notification')
    def test_send_notification_uses_enabled_channels(self, mock_webhook, mock_email):
        send_notification.run(self.message)

        mock_email.assert_called_once()
        mock_webhook.assert_called_once_with(
            mock_email.call_args[0][0], 'https://example.com/webhook'
        )

    @patch('api.tasks.send_email_notification')
    @patch('api.tasks.send_webhook_notification')
    def test_send_notification_respects_category_preference(self, mock_webhook, mock_email):
        self.preference.notify_security = False
        self.preference.save(update_fields=['notify_security'])

        send_notification.run(self.message)

        mock_email.assert_not_called()
        mock_webhook.assert_not_called()

    @patch('api.tasks.send_email_notification')
    @patch('api.tasks.send_webhook_notification')
    def test_send_notification_uses_default_true_for_unknown_category(
        self, mock_webhook, mock_email
    ):
        self.message.category = 'unknown'
        self.message.save(update_fields=['category'])

        send_notification.run(self.message)

        mock_email.assert_called_once()
        mock_webhook.assert_called_once_with(
            mock_email.call_args[0][0], 'https://example.com/webhook'
        )

    @patch('api.tasks.send_email_notification')
    @patch('api.tasks.send_webhook_notification')
    @patch('api.tasks.logger')
    def test_send_notification_without_preference_sends_email_only(
        self, mock_logger, mock_webhook, mock_email
    ):
        self.preference.delete()
        # Refresh to clear cached related object
        self.message.refresh_from_db()
        self.message.user = User.objects.get(pk=self.user.pk)

        send_notification.run(self.message)

        mock_email.assert_called_once()
        mock_webhook.assert_not_called()
        mock_logger.info.assert_called_once_with(
            'Send email notification for message %s without user preference',
            self.message.id,
        )

    @patch('api.tasks.send_webhook_notification', side_effect=RuntimeError('boom'))
    def test_send_notification_propagates_dispatch_error(self, _mock_webhook):
        with self.assertRaises(RuntimeError):
            send_notification.run(self.message)

    @patch('api.tasks.send_email_notification')
    @patch('api.tasks.send_webhook_notification')
    def test_send_notification_supports_alert_category_with_singular_field(
        self, mock_webhook, mock_email
    ):
        self.message.category = 'alert'
        self.message.save(update_fields=['category'])
        self.preference.notify_alert = False
        self.preference.save(update_fields=['notify_alert'])

        send_notification.run(self.message)

        mock_email.assert_not_called()
        mock_webhook.assert_not_called()
