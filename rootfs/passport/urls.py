"""passport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url, re_path
from django.contrib import admin
from django.views.generic.base import TemplateView
from api.views import LivenessCheckView, ReadinessCheckView
from . import views

if settings.ADMIN_ENABLED:
    urlpatterns = [path('admin/', admin.site.urls)]
else:
    urlpatterns = []

urlpatterns += [
    url(r'^healthz$', LivenessCheckView.as_view()),
    url(r'^readiness$', ReadinessCheckView.as_view()),
    re_path(r"settings/?$", views.SettingsViewSet.as_view({'get': 'retrieve'})),
    re_path(r"^user/", include('api.urls')),
    re_path(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'.*', TemplateView.as_view(template_name="index.html")),
]
