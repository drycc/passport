from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from api import views
from api.views import RegisterView, ActivateAccount, RegisterDoneView, \
    ActivateAccountDoneView, ActivateAccountFailView, LoginDoneView

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    re_path(r'^$', views.index, name='index'),

    re_path(r'^', include(router.urls)),

    re_path(r'user/register/?$', RegisterView.as_view(), name='register'),
    re_path(r'user/activate/(?P<uidb64>.+)/(?P<token>.+)/?$',
            ActivateAccount.as_view(), name='user_activate_account'),
    re_path(r'user/register/done/?$', RegisterDoneView.as_view(),
            name='user_register_done'),
    re_path(r'user/activate/done/?$', ActivateAccountDoneView.as_view(),
            name='user_activate_account_done'),
    re_path(r'user/activate/fail/?$', ActivateAccountFailView.as_view(),
            name='user_activate_account_done'),
    re_path(r'user/password_reset/?$', views.UserPasswordResetView.as_view(),
            name='user_password_reset'),
    re_path(r'user/password_reset/done/?$',
            views.UserPasswordResetDoneView.as_view(),
            name='user_password_reset_done'),
    re_path(r'user/reset/<uidb64>/<token>/?$',
            views.UserPasswordResetConfirmView.as_view(),
            name='user_password_reset_confirm'),
    re_path(r'user/reset/done/?$',
            views.UserPasswordResetCompleteView.as_view(),
            name='user_password_reset_complete'),
    re_path(r'user/password_change/?$', views.UserPasswordChangeView.as_view(),
            name='user_password_change'),
    re_path(r'user/password_change/done/?$',
            views.UserPasswordchangeDoneView.as_view(),
            name='user_password_change_done'),
    # re_path(r'^user/login/?$', views.login_view, name='login'),
    re_path(r'^user/login/?$', views.UserLoginView.as_view(), name='user_login'),
    re_path(r'^user/logout/?$', views.UserLogoutView.as_view(), name='user_logout'),

    re_path(r'grants/?$',
            views.UserGrantsTemplateView.as_view({'get': 'retrieve'}), name='user_grants'),
    re_path(r'grants/(?P<pk>.+)/?$',
            views.UserGrantDeleteView.as_view({'delete': 'destroy'}), name='user_grants'),
    re_path(r'tokens/?$',
            views.UserTokensTemplateView.as_view({'get': 'retrieve'}), name='user_tokens'),
    re_path(r'tokens/(?P<pk>.+)/?$',
            views.UserTokenDeleteView.as_view({'delete': 'destroy'}), name='user_grants'),
    re_path(r'users/logs/?$',
            views.UserLogsView.as_view({'get': 'retrieve'}), name='user_logs'),

    re_path(r'login/done/?$', LoginDoneView.as_view(), name='login_done'),

    re_path(r'accounts/', include('django.contrib.auth.urls')),

    re_path(r'oauth/',
            include('oauth2_provider.urls', namespace='oauth2_provider')),

    re_path(r'users/?$', views.UserDetailView.as_view({'get': 'retrieve'})),
    re_path(r'users/emails/?$',
            views.UserEmailView.as_view({'get': 'retrieve'})),


]
