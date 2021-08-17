from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from api import views
from api.views import RegisterView, ActivateAccount, RegisterDoneView, \
    ActivateAccountDoneView, ActivateAccountFailView, LoginDoneView

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^info/?$',
            views.UserDetailView.as_view({'get': 'retrieve', 'put': 'update'})),
    re_path(r'register/?$', RegisterView.as_view(), name='register'),
    re_path(r'activate/(?P<uidb64>.+)/(?P<token>.+)/?$',
            ActivateAccount.as_view(), name='user_activate_account'),
    re_path(r'register/done/?$', RegisterDoneView.as_view(),
            name='user_register_done'),
    re_path(r'activate/done/?$', ActivateAccountDoneView.as_view(),
            name='user_activate_account_done'),
    re_path(r'activate/fail/?$', ActivateAccountFailView.as_view(),
            name='user_activate_account_done'),
    re_path(r'password_reset/?$', views.UserPasswordResetView.as_view(),
            name='user_password_reset'),
    re_path(r'password_reset/done/?$',
            views.UserPasswordResetDoneView.as_view(),
            name='user_password_reset_done'),
    re_path(r'reset/<uidb64>/<token>/?$',
            views.UserPasswordResetConfirmView.as_view(),
            name='user_password_reset_confirm'),
    re_path(r'reset/done/?$',
            views.UserPasswordResetCompleteView.as_view(),
            name='user_password_reset_complete'),
    re_path(r'login/?$', views.UserLoginView.as_view(), name='user_login'),
    re_path(r'login/done/?$', LoginDoneView.as_view(), name='login_done'),
    re_path(r'logout/?$', views.UserLogoutView.as_view(), name='user_logout'),

    re_path(r'tokens/?$',
            views.UserTokensTemplateView.as_view({'get': 'retrieve'}),
            name='user_tokens'),
    re_path(r'tokens/(?P<pk>.+)/?$',
            views.UserTokenDeleteView.as_view({'delete': 'destroy'}),
            name='user_grants'),
    re_path(r'email/?$', views.UserEmailView.as_view({'get': 'retrieve'})),
    re_path(r'password/?$',
            views.UserAccountPasswordView.as_view({'put': 'update'}),
            name='user_account_update_password'),

]
