from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class NormalUserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for objects filtered by their 'owner' attribute.

    To use it, at minimum you'll need to provide the `serializer_class` attribute and
    the `model` attribute shortcut.
    """
    permission_classes = [IsAuthenticated]
