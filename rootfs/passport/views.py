from django.conf import settings
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class AppSettingsViewSet(GenericViewSet):

    permission_classes = (AllowAny, )

    def retrieve(self, request, *args, **kwargs):
        return Response(data={
            "legal": getattr(settings, 'LEGAL_ENABLED', False),
            "dashboard_url": getattr(settings, 'DASHBOARD_URL', '/'),
            "contact_support_url": getattr(
                settings, 'CONTACT_SUPPORT_URL',
                'https://community.drycc.cc/'
            ),
            "registration_enabled": getattr(settings, 'REGISTRATION_ENABLED', False),
        })
