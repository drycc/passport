from django.conf import settings
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class SettingsViewSet(GenericViewSet):

    permission_classes = (AllowAny, )

    def retrieve(self, request, *args, **kwargs):
        return Response(data={
            "legal": settings.LEGAL_ENABLED,
            "registration_enabled": settings.REGISTRATION_ENABLED,
        })
