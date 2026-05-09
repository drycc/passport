import os
import json
import random
import string
import pathlib
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.management.base import BaseCommand
from oauth2_provider.models import get_application_model


User = get_user_model()
Application = get_application_model()
secrets_path = "/var/run/secrets/drycc/passport"


class Command(BaseCommand):
    """Management command for create Oauth2 application.

    Credential resolution order for ``client_id`` / ``client_secret``:

    1. Explicit value from the init-applications JSON file (highest priority,
       lets operators pin credentials via ``--set initApplications[...]``).
    2. Mounted Kubernetes secret file at
       ``/var/run/secrets/drycc/passport/drycc-passport-<name>-<key|secret>``.
       This is the source of truth for credentials that the chart's
       ``passport-creds`` Secret already exposes to every consumer (controller,
       grafana, builder, manager, ...). Reading it here keeps the DB and the
       Secret consistent for *every* application, including m2m apps that
       have no public sub-domain (``prefix == ""``).
    3. Newly generated random string (only when neither of the above is
       available, e.g. local dev without the volume mount).

    Note: ``prefix`` only controls how ``redirect_uri`` is composed. It is
    intentionally NOT used to gate credential discovery -- m2m applications
    legitimately have an empty prefix.
    """

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
            client_id = self._get_creds(item, "key", 40)
            client_secret = self._get_creds(item, "secret", 60)
            defaults = {
                'client_id': client_id,
                'user': user,
                'redirect_uris': self._get_redirect_uri(item),
                'authorization_grant_type': item.get('grant_type', 'public'),
                'client_type': item.get('client_type', 'public'),
                'allowed_scopes': item.get('allowed_scopes', ''),
                'algorithm': 'RS256',
            }
            existing = Application.objects.filter(name=name.lower()).first()
            secret_unchanged = (
                existing is not None
                and check_password(client_secret, existing.client_secret)
            )
            if not secret_unchanged:
                defaults['client_secret'] = client_secret
            _, created = Application.objects.update_or_create(
                name=name.lower(), defaults=defaults,
            )
            if created:
                self.stdout.write('Drycc %s app created' % name)
            else:
                self.stdout.write('Drycc %s app updated' % name)

    def _get_creds(self, item, suffix, size):
        name = item["name"]
        secret = item.get(suffix)
        if secret:
            self.stdout.write(
                '[%s/%s] credential source: init-config' % (name, suffix))
            return secret

        default_secret_path = os.path.join(
            secrets_path, "drycc-passport-%s-%s" % (name, suffix))
        if os.path.exists(default_secret_path):
            # ``.strip()`` defends against trailing newlines that some
            # tooling adds when materialising secrets onto disk.
            secret = pathlib.Path(default_secret_path).read_text().strip()
            self.stdout.write(
                '[%s/%s] credential source: mounted-file (%s)'
                % (name, suffix, default_secret_path))
            return secret

        secret = ''.join(random.choice(string.ascii_letters) for _ in range(size))
        self.stdout.write(
            '[%s/%s] credential source: generated-random '
            '(no init value, no mounted file)' % (name, suffix))
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
