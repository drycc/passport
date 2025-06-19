from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):

    oidc_claim_scope = OAuth2Validator.oidc_claim_scope
    oidc_claim_scope.update({
        "id": "profile",
        "name": "profile",
        "username": "profile",
        "email": "email",
        "first_name": "profile",
        "last_name": "profile",
        "is_staff": "profile",
        "is_active": "profile",
        "is_superuser": "profile",
        "preferred_username": "profile",
    })

    def get_additional_claims(self, request):
        claims = super().get_additional_claims(request)
        claims["id"] = request.user.id
        claims["name"] = request.user.username
        claims["username"] = request.user.username
        claims["email"] = request.user.email
        claims["first_name"] = request.user.first_name
        claims["last_name"] = request.user.last_name
        claims["is_staff"] = request.user.is_staff
        claims["is_active"] = request.user.is_active
        claims["is_superuser"] = request.user.is_superuser
        claims["preferred_username"] = request.user.username
        return claims
