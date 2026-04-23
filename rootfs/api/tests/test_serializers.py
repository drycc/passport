from django.contrib.auth import get_user_model
from django.test import TestCase

from api.models import Message, MessagePreference
from api.serializers import ListSerializer, MessagePreferenceSerializer, MessageSerializer

User = get_user_model()


class SerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='serializer-user',
            email='serializer@example.com',
            password='password123',
        )
        self.message = Message.objects.create(
            user=self.user,
            category='system',
            title='Serializer message',
            content='Serializer content',
            full_content='Serializer full content',
            severity='info',
        )
        self.preference = MessagePreference.objects.create(
            user=self.user,
            email_alerts=True,
            push_alerts=False,
            webhook_url='',
            notify_security=True,
            notify_system=True,
            notify_product=True,
            notify_alert=True,
            notify_service=True,
        )

    def test_list_serializer_validate_section(self):
        result = ListSerializer.validate_section('1,2')
        self.assertEqual(len(result), 2)

    def test_message_serializer_contains_expected_fields(self):
        data = MessageSerializer(self.message).data
        self.assertEqual(data['category'], 'system')
        self.assertEqual(data['title'], 'Serializer message')
        self.assertIn('date', data)

    def test_message_preference_serializer_contains_singular_alert_field(self):
        data = MessagePreferenceSerializer(self.preference).data
        self.assertIn('notify_alert', data)
        self.assertTrue(data['notify_alert'])
