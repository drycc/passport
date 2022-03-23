from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^info/?$',
            views.UserDetailView.as_view({'get': 'retrieve', 'put': 'update'})),
    re_path(r'update/(?P<uidb64>.+)/(?P<token>.+)/?$',
            views.UpdateAccount.as_view(), name='user_update_account'),
    re_path(r'^avatar/(?P<username>[-_\w]+)/?$',
            views.UserAvatarViewSet.as_view({'get': 'avatar'})),
    re_path(r'registration/?$', views.RegistrationView.as_view(), name='registration'),
    re_path(r'activate/(?P<uidb64>.+)/(?P<token>.+)/?$',
            views.ActivateAccount.as_view(), name='user_activate_account'),
    re_path(r'registration/done/?$', views.RegistrationDoneView.as_view(),
            name='user_registration_done'),
    re_path(r'activate/done/?$', views.ActivateAccountDoneView.as_view(),
            name='user_activate_account_done'),
    re_path(r'activate/fail/?$', views.ActivateAccountFailView.as_view(),
            name='user_activate_account_done'),
    re_path(r'password_reset/?$', views.UserPasswordResetView.as_view(),
            name='user_password_reset'),
    re_path(r'password_reset/done/?$',
            views.UserPasswordResetDoneView.as_view(),
            name='user_password_reset_done'),
    re_path(r'reset/(?P<uidb64>.+)/(?P<token>.+)/?$',
            views.UserPasswordResetConfirmView.as_view(),
            name='user_password_reset_confirm'),
    re_path(r'reset/done/?$',
            views.UserPasswordResetCompleteView.as_view(),
            name='user_password_reset_complete'),
    re_path(r'login/?$', views.UserLoginView.as_view(), name='user_login'),
    re_path(r'login/done/?$', views.LoginDoneView.as_view(), name='login_done'),
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
