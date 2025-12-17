from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from oauth2_provider.models import AbstractApplication
from .validators import UsernameValidator, OrganizationNameValidator


class User(AbstractUser):
    username_validator = UsernameValidator()
    email = models.EmailField(_('email address'), unique=True)


class Application(AbstractApplication):

    def allows_grant_type(self, *grant_types):
        return self.GRANT_AUTHORIZATION_CODE in grant_types or super().allows_grant_type(
            *grant_types
        )


class Organization(models.Model):
    name = models.SlugField(
        _("organization name"),
        max_length=255,
        unique=True,
        validators=[OrganizationNameValidator()],
    )
    email = models.EmailField(_("email address"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrganizationMember(models.Model):
    role_choices = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=role_choices)
    alerts = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return f"{self.user.username} - {self.organization.name} ({self.role})"


class OrganizationInvitation(models.Model):
    email = models.EmailField(_("email address"))
    token = models.CharField(max_length=128, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(_("accepted"), default=False)

    class Meta:
        unique_together = ('email', 'organization')

    def accept(self):
        user = User.objects.filter(email=self.email).first()
        if not user or self.accepted:
            return
        OrganizationMember.objects.get_or_create(
            user=user, organization=self.organization, defaults={'role': 'member'})
        self.accepted = True
        self.save()

    @classmethod
    def bulk_accept_by_email(cls, email):
        for invitation in OrganizationInvitation.objects.filter(email=email, accepted=False):
            invitation.accept()

    def __str__(self):
        return f"Invitation for {self.email} to join {self.organization.name}"
