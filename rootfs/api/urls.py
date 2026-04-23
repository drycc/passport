from django.urls import re_path, include
from rest_framework.routers import SimpleRouter

from api.views import web, api
from passport.views import AppSettingsViewSet


class OptionalSlashRouter(SimpleRouter):
    """Router that accepts both trailing-slash and no-trailing-slash URLs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register(r'user/messages', api.UserMessageViewSet, basename='user_messages')
router.register(r'user/identities', api.UserIdentityViewSet, basename='user_identities')

urlpatterns = [
    re_path(r'^', include(router.urls)),
    # Settings URL (moved from main urls.py)
    re_path(r'^settings/?$', AppSettingsViewSet.as_view({'get': 'retrieve'})),
    # User URLs (add user prefix)
    re_path(r'^user/info/?$',
            api.UserDetailView.as_view({'get': 'retrieve', 'put': 'update'})),
    re_path(r'^user/update/(?P<uidb64>.+)/(?P<token>.+)/?$',
            web.UpdateAccount.as_view(), name='user_update_account'),
    re_path(r'^user/registration/?$', web.RegistrationView.as_view(), name='registration'),
    re_path(r'^user/activate/(?P<uidb64>.+)/(?P<token>.+)/?$',
            web.ActivateAccount.as_view(), name='user_activate_account'),
    re_path(r'^user/registration/done/?$', web.RegistrationDoneView.as_view(),
            name='user_registration_done'),
    re_path(r'^user/activate/done/?$', web.ActivateAccountDoneView.as_view(),
            name='user_activate_account_done'),
    re_path(r'^user/activate/fail/?$', web.ActivateAccountFailView.as_view(),
            name='user_activate_account_done'),
    re_path(r'^oauth/callback/?$', web.OAuthCallbackTemplateView.as_view(),
            name='oauth_callback'),
    re_path(r'^user/password_reset/?$', web.UserPasswordResetView.as_view(),
            name='user_password_reset'),
    re_path(r'^user/password_reset/done/?$',
            web.UserPasswordResetDoneView.as_view(),
            name='user_password_reset_done'),
    re_path(r'^user/reset/(?P<uidb64>.+)/(?P<token>.+)/?$',
            web.UserPasswordResetConfirmView.as_view(),
            name='user_password_reset_confirm'),
    re_path(r'^user/reset/done/?$',
            web.UserPasswordResetCompleteView.as_view(),
            name='user_password_reset_complete'),
    re_path(r'^user/login/?$', web.UserLoginView.as_view(), name='user_login'),
    re_path(r'^user/login/done/?$', web.LoginDoneView.as_view(), name='login_done'),
    re_path(r'^user/logout/?$', web.UserLogoutView.as_view(), name='user_logout'),
    re_path(r'^user/tokens/?$',
            api.UserTokensView.as_view({'get': 'list'}),
            name='user_tokens'),
    re_path(r'^user/tokens/(?P<pk>.+)/?$',
            api.UserTokensView.as_view({'delete': 'destroy'}),
            name='user_grants'),
    re_path(r'^user/email/?$', api.UserEmailView.as_view({'get': 'retrieve'})),
    re_path(r'^user/password/?$',
            api.UserAccountPasswordView.as_view(),
            name='user_account_update_password'),
    re_path(r'^user/identity-providers/?$',
            api.IdentityProviderView.as_view(), name='user_identity_providers'),
    re_path(r'^user/oauth/pending/?$',
            api.OAuthPendingView.as_view(), name='user_oauth_pending'),
    re_path(r'^user/oauth/create/?$',
            api.OAuthCreateUserView.as_view(), name='user_oauth_create'),
    re_path(r'^user/message-preferences/?$',
            api.UserMessagePreferenceViewSet.as_view(
                {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}),
            name='user_message_preferences'),
]
