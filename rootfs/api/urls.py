from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from api import views
from passport.views import SettingsViewSet

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    # Settings URL (moved from main urls.py)
    re_path(r'^settings/?$', SettingsViewSet.as_view({'get': 'retrieve'})),
    # User URLs (add user prefix)
    re_path(r'^user/info/?$',
            views.UserDetailView.as_view({'get': 'retrieve', 'put': 'update'})),
    re_path(r'^user/update/(?P<uidb64>.+)/(?P<token>.+)/?$',
            views.UpdateAccount.as_view(), name='user_update_account'),
    re_path(r'^user/avatar/(?P<username>[-_\w]+)/?$',
            views.UserAvatarViewSet.as_view({'get': 'avatar'})),
    re_path(r'^user/registration/?$', views.RegistrationView.as_view(), name='registration'),
    re_path(r'^user/activate/(?P<uidb64>.+)/(?P<token>.+)/?$',
            views.ActivateAccount.as_view(), name='user_activate_account'),
    re_path(r'^user/registration/done/?$', views.RegistrationDoneView.as_view(),
            name='user_registration_done'),
    re_path(r'^user/activate/done/?$', views.ActivateAccountDoneView.as_view(),
            name='user_activate_account_done'),
    re_path(r'^user/activate/fail/?$', views.ActivateAccountFailView.as_view(),
            name='user_activate_account_done'),
    re_path(r'^user/password_reset/?$', views.UserPasswordResetView.as_view(),
            name='user_password_reset'),
    re_path(r'^user/password_reset/done/?$',
            views.UserPasswordResetDoneView.as_view(),
            name='user_password_reset_done'),
    re_path(r'^user/reset/(?P<uidb64>.+)/(?P<token>.+)/?$',
            views.UserPasswordResetConfirmView.as_view(),
            name='user_password_reset_confirm'),
    re_path(r'^user/reset/done/?$',
            views.UserPasswordResetCompleteView.as_view(),
            name='user_password_reset_complete'),
    re_path(r'^user/login/?$', views.UserLoginView.as_view(), name='user_login'),
    re_path(r'^user/login/done/?$', views.LoginDoneView.as_view(), name='login_done'),
    re_path(r'^user/logout/?$', views.UserLogoutView.as_view(), name='user_logout'),

    re_path(r'^user/tokens/?$',
            views.UserTokensView.as_view({'get': 'list'}),
            name='user_tokens'),
    re_path(r'^user/tokens/(?P<pk>.+)/?$',
            views.UserTokensView.as_view({'delete': 'destroy'}),
            name='user_grants'),
    re_path(r'^user/email/?$', views.UserEmailView.as_view({'get': 'retrieve'})),
    re_path(r'^user/password/?$',
            views.UserAccountPasswordView.as_view({'put': 'update'}),
            name='user_account_update_password'),

    # Organization management URLs (keep orgs prefix, no user prefix)
    re_path(r'^orgs/?$',
            views.OrganizationViewSet.as_view({'get': 'list', 'post': 'create'}),
            name='organization_list'),
    re_path(r'^orgs/(?P<name>[-_\w]+)/?$',
            views.OrganizationViewSet.as_view(
                {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
            name='organization_detail'),
    re_path(r'^orgs/(?P<name>[-_\w]+)/members/?$',
            views.OrganizationMemberViewSet.as_view({'get': 'list'}),
            name='organization_member_list'),
    re_path(r'^orgs/(?P<name>[-_\w]+)/members/(?P<user>[-_\w]+)/?$',
            views.OrganizationMemberViewSet.as_view(
                {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
            name='organization_member_detail'),
    re_path(r'^orgs/(?P<name>[-_\w]+)/invitations/?$',
            views.OrganizationInvitationViewSet.as_view({'get': 'list', 'post': 'create'}),
            name='organization_invitation_list'),
    re_path(r'^orgs/(?P<name>[-_\w]+)/invitations/(?P<uid>[-_\w]+)/?$',
            views.OrganizationInvitationViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
            name='organization_invitation_detail'),
]
