import os
import json
import random
import string
import pathlib
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from oauth2_provider.models import Application


User = get_user_model()
secrets_path = "/var/run/secrets/drycc/passport"


class Command(BaseCommand):
    """Management command for create Oauth2 application"""

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--path', dest='path', default=None,
            help='Specifies the path for the secret.',
        )

    def handle(self, *args, **options):
        base_path = options.get('path', '')
        user = User.objects.filter(is_superuser=True).first()
        for item in json.loads(pathlib.Path(base_path).read_text()):
            name = item["name"]
            key = self._get_creds(item, "key", 40)
            secret = self._get_creds(item, "secret", 60)
            redirect_uri = self._get_redirect_uri(item)
            _, updated = Application.objects.update_or_create(
                name=name.lower(),
                defaults={
                    'client_id': key,
                    'client_secret': secret,
                    'user': user,
                    'redirect_uris': redirect_uri,
                    'authorization_grant_type': 'authorization-code',
                    'client_type': 'public',
                    'algorithm': 'RS256'
                }
            )
            if updated:
                self.stdout.write('Drycc % app created' % name)
            else:
                self.stdout.write('Drycc % app updated' % name)

    def _get_creds(self, item, suffix, size):
        name, secret, prefix = item["name"], item[suffix], item["prefix"]
        if not secret:
            default_secret_path = os.path.join(
                secrets_path, "drycc-passport-%s-%s" % (name, suffix))
            if prefix and os.path.exists(default_secret_path):
                secret = pathlib.Path(default_secret_path).read_text()
            else:
                secret = ''.join([random.choice(string.ascii_letters) for _ in range(size)])
        return secret

    def _get_redirect_uri(self, item):
        prefix = item["prefix"]
        domain = os.environ.get("PLATFORM_DOMAIN")
        redirect_uri = item["redirect_uri"]
        if prefix:
            if os.environ.get("CERT_MANAGER_ENABLED") == "true":
                redirect_uri = f"https://{prefix}.{domain}{redirect_uri}"
            else:
                redirect_uri = f"http://{prefix}.{domain}{redirect_uri}"
        return redirect_uri
