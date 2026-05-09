import json
import os
import tempfile
from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.management import call_command
from django.test import TestCase
from oauth2_provider.models import get_application_model

from api.management.commands import create_oauth2_application as cmd_module

User = get_user_model()
Application = get_application_model()


class CreateOauth2ApplicationTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='create-oauth2-admin',
            email='create-oauth2-admin@example.com',
            password='password123',
        )
        self.tmpdir = tempfile.mkdtemp()
        self.secrets_dir = tempfile.mkdtemp()
        self._secrets_patch = mock.patch.object(
            cmd_module, 'secrets_path', self.secrets_dir,
        )
        self._secrets_patch.start()
        self.addCleanup(self._secrets_patch.stop)

    def _write_init_file(self, items):
        path = os.path.join(self.tmpdir, 'init-applications.json')
        with open(path, 'w') as f:
            json.dump(items, f)
        return path

    def _write_secret_file(self, name, suffix, value):
        path = os.path.join(
            self.secrets_dir, 'drycc-passport-%s-%s' % (name, suffix))
        with open(path, 'w') as f:
            f.write(value)
        return path

    def _run(self, items):
        path = self._write_init_file(items)
        out = StringIO()
        call_command('create_oauth2_application', '--path', path, stdout=out)
        return out.getvalue()

    def _m2m_app(self, **overrides):
        item = {
            'name': 'builder',
            'key': '',
            'secret': '',
            'prefix': '',
            'grant_type': 'client-credentials',
            'client_type': 'confidential',
            'allowed_scopes': 'controller:hook',
            'redirect_uri': '',
        }
        item.update(overrides)
        return item

    def test_m2m_reads_credentials_from_mounted_secret_files(self):
        self._write_secret_file('builder', 'key', 'mounted-key-value')
        self._write_secret_file('builder', 'secret', 'mounted-secret-value\n')

        self._run([self._m2m_app()])

        app = Application.objects.get(name='builder')
        self.assertEqual(app.client_id, 'mounted-key-value')
        self.assertTrue(check_password('mounted-secret-value', app.client_secret))

    def test_subdomain_app_reads_credentials_from_mounted_secret_files(self):
        self._write_secret_file('grafana', 'key', 'gf-key')
        self._write_secret_file('grafana', 'secret', 'gf-secret')

        self._run([{
            'name': 'grafana',
            'key': '',
            'secret': '',
            'prefix': 'drycc-grafana',
            'grant_type': 'internal',
            'client_type': 'confidential',
            'allowed_scopes': 'openid profile email',
            'redirect_uri': '/oauth2/callback',
        }])

        app = Application.objects.get(name='grafana')
        self.assertEqual(app.client_id, 'gf-key')
        self.assertTrue(check_password('gf-secret', app.client_secret))

    def test_falls_back_to_random_when_no_mount_and_no_init_value(self):
        self._run([self._m2m_app()])

        app = Application.objects.get(name='builder')
        self.assertEqual(len(app.client_id), 40)
        self.assertNotEqual(app.client_id, '')
        self.assertNotEqual(app.client_secret, '')

    def test_init_config_value_takes_precedence_over_mount(self):
        self._write_secret_file('builder', 'key', 'mount-key')
        self._write_secret_file('builder', 'secret', 'mount-secret')

        self._run([self._m2m_app(key='cfg-key', secret='cfg-secret')])

        app = Application.objects.get(name='builder')
        self.assertEqual(app.client_id, 'cfg-key')
        self.assertTrue(check_password('cfg-secret', app.client_secret))

    def test_idempotent_when_mount_unchanged(self):
        self._write_secret_file('builder', 'key', 'stable-key')
        self._write_secret_file('builder', 'secret', 'stable-secret')

        self._run([self._m2m_app()])
        first = Application.objects.get(name='builder')
        first_id = first.client_id
        first_hashed_secret = first.client_secret

        self._run([self._m2m_app()])
        second = Application.objects.get(name='builder')

        self.assertEqual(second.client_id, first_id)
        self.assertEqual(second.client_secret, first_hashed_secret)
        self.assertTrue(check_password('stable-secret', second.client_secret))
        self.assertEqual(Application.objects.filter(name='builder').count(), 1)

    def test_logs_credential_source(self):
        self._write_secret_file('builder', 'key', 'k')
        self._write_secret_file('builder', 'secret', 's')

        out = self._run([self._m2m_app()])

        self.assertIn('[builder/key] credential source: mounted-file', out)
        self.assertIn('[builder/secret] credential source: mounted-file', out)
        self.assertIn('Drycc builder app created', out)
