from django.utils import timezone
from rest_framework import permissions

from oauth2_provider.models import AccessToken


class HasOAuthScope(permissions.BasePermission):
    """
    Object-level permission to allow only requests with specific OAuth scopes.
    The required scopes are defined on the view as `required_oauth_scopes = ['scope1', 'scope2']`
    """
    def has_permission(self, request, view):
        required_oauth_scopes = getattr(view, 'required_oauth_scopes', [])
        if not required_oauth_scopes:
            return True

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            token_string = parts[1]
        else:
            return False

        scopes = self.get_token_scopes(token_string)
        return set(required_oauth_scopes).issubset(scopes)

    def get_token_scopes(self, token_string):
        try:
            access_token = AccessToken.objects.get(token=token_string, expires__gt=timezone.now())
            return set(access_token.scope.split())
        except AccessToken.DoesNotExist:
            return set()
