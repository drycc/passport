import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from oauth2_provider.models import Application


class Command(BaseCommand):
    """Management command for create Oauth2 application"""

    def handle(self, *args, **options):
        app_list = [{
            "name": "CONTROLLER",
            "redirect_uri": f"{os.environ.get('DRYCC_CONTROLLER_DOMAIN')}/v2/complete/drycc/"  # noqa
        }]
        if os.environ.get('GRAFANA_ON_CLUSTER') == "true":
            app_list.append({
                "name": "GRAFANA",
                 "redirect_uri": f"{os.environ.get('DRYCC_MONITOR_GRAFANA_DOMAIN')}/login/generic_oauth"  # noqa
            })

        for app in app_list:
            client_id = os.environ.get(
                f'SOCIAL_AUTH_DRYCC_{app["name"]}_KEY') if os.environ.get(
                f'SOCIAL_AUTH_DRYCC_{app["name"]}_KEY') else None
            client_secret = os.environ.get(
                f'SOCIAL_AUTH_DRYCC_{app["name"]}_SECRET') if os.environ.get(
                f'SOCIAL_AUTH_DRYCC_{app["name"]}_SECRET') else None
            if not all([client_id, client_secret]):
                self.stdout.write('client_id or client_secret non-existent')
                return
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                self.stdout.write("Cannot create because there is no superuser")
            application, updated = Application.objects.update_or_create(
                name='Drycc ' + app["name"].title(),
                defaults={
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'user': user,
                    'redirect_uris': app["redirect_uri"],
                    'authorization_grant_type': 'authorization-code',
                    'client_type': 'Public',
                    'algorithm': 'RS256'
                }
            )
            if updated:
                self.stdout.write(f'Drycc {app["name"]} app created')
            else:
                self.stdout.write(f'Drycc {app["name"]} app updated')
