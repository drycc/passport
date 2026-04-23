from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from oauth2_provider.models import AbstractApplication
from .validators import UsernameValidator


class User(AbstractUser):
    username_validator = UsernameValidator()
    email = models.EmailField(_('email address'), unique=True)


class Application(AbstractApplication):

    def allows_grant_type(self, *grant_types):
        return self.GRANT_AUTHORIZATION_CODE in grant_types or super().allows_grant_type(
            *grant_types
        )


class Message(models.Model):
    CATEGORY_CHOICES = [
        ('system', _('System')),
        ('product', _('Product Updates')),
        ('security', _('Security')),
        ('alert', _('Alerts')),
        ('service', _('Service')),
    ]

    SEVERITY_CHOICES = [
        ('info', _('Info')),
        ('warning', _('Warning')),
        ('error', _('Error')),
        ('success', _('Success')),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('user')
    )
    category = models.CharField(
        _('category'),
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='system'
    )
    title = models.CharField(_('title'), max_length=255)
    content = models.TextField(_('content'))
    full_content = models.TextField(_('full content'), blank=True)
    severity = models.CharField(
        _('severity'),
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='info'
    )
    is_read = models.BooleanField(_('is read'), default=False)
    action_link = models.CharField(
        _('action link'),
        max_length=500,
        blank=True
    )
    action_text = models.CharField(
        _('action text'),
        max_length=255,
        blank=True
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __str__(self):
        return f"[{self.category}] {self.title}"


class MessagePreference(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='message_preference',
        verbose_name=_('user')
    )
    email_alerts = models.BooleanField(
        _('email alerts'),
        default=True
    )
    push_alerts = models.BooleanField(
        _('push alerts'),
        default=False
    )
    webhook_url = models.URLField(
        _('webhook url'),
        max_length=500,
        blank=True
    )
    notify_security = models.BooleanField(
        _('notify security'),
        default=True
    )
    notify_system = models.BooleanField(
        _('notify system'),
        default=True
    )
    notify_product = models.BooleanField(
        _('notify product'),
        default=True
    )
    notify_alert = models.BooleanField(
        _('notify alert'),
        default=True
    )
    notify_service = models.BooleanField(
        _('notify service'),
        default=True
    )

    class Meta:
        verbose_name = _('message preference')
        verbose_name_plural = _('message preferences')

    def __str__(self):
        return f"{self.user.username}'s message preference"
