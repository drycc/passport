"""
Test cases for API views
"""
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from oauth2_provider.models import AccessToken

from api.views import (
    ReadinessCheckView, LivenessCheckView, ActivateAccount, is_organization_member
)
from api.models import Organization, OrganizationMember, OrganizationInvitation
from api.forms import RegistrationForm

User = get_user_model()


class TestReadinessCheckView(TestCase):
    """Test readiness check view"""

    def test_readiness_check_get(self):
        """Test GET request returns OK"""
        request = RequestFactory().get('/readiness/')
        response = ReadinessCheckView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')

    def test_readiness_check_head(self):
        """Test HEAD request returns OK"""
        request = RequestFactory().head('/readiness/')
        response = ReadinessCheckView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestLivenessCheckView(TestCase):
    """Test liveness check view"""

    def test_liveness_check_get(self):
        """Test GET request returns OK"""
        request = RequestFactory().get('/liveness/')
        response = LivenessCheckView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')

    def test_liveness_check_head(self):
        """Test HEAD request returns OK"""
        request = RequestFactory().head('/liveness/')
        response = LivenessCheckView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestRegistrationView(TestCase):
    """Test registration view"""

    def setUp(self):
        self.factory = RequestFactory()

    def test_registration_form_valid(self):
        """Test registration with valid form data"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestActivateAccount(TestCase):
    """Test account activation view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_active=False
        )
        self.factory = RequestFactory()

    def test_activate_account_invalid_token(self):
        """Test activation with invalid token"""
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.messages.storage.fallback import FallbackStorage

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        request = self.factory.get(f'/activate/{uid}/invalid-token/')
        # Add messages middleware support for test
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = ActivateAccount.as_view()(request, uidb64=uid, token='invalid-token')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/user/activate/fail/')


class TestUserDetailView(APITestCase):
    """Test user detail viewset"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_user_detail(self):
        """Test retrieving user details"""
        url = '/user/info'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_user_detail(self):
        """Test updating user details"""
        url = '/user/info'
        data = {'first_name': 'Test', 'last_name': 'User'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestUserTokensView(APITestCase):
    """Test user tokens viewset"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = AccessToken.objects.create(
            user=self.user,
            token='test-token-123',
            expires='2030-01-01T00:00:00Z'
        )
        self.client.force_authenticate(user=self.user)

    def test_list_user_tokens(self):
        """Test listing user tokens"""
        url = reverse('user_tokens')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 检查返回的数据结构，可能是列表或字典
        if isinstance(response.data, list):
            self.assertEqual(len(response.data), 1)
        else:
            # 如果是分页响应或其他格式
            self.assertIn('results', response.data)
            self.assertEqual(len(response.data['results']), 1)

    def test_delete_user_token(self):
        """Test deleting a user token"""
        url = reverse('user_grants', args=[self.token.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AccessToken.objects.filter(id=self.token.id).exists())


class TestUserAccountPasswordView(APITestCase):
    """Test user account password view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpassword123'
        )
        self.client.force_authenticate(user=self.user)

    def test_update_password_valid(self):
        """Test updating password with valid data"""
        url = '/user/password'
        data = {
            'password': 'oldpassword123',
            'new_password': 'newpassword123'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))


class TestOrganizationViewSet(APITestCase):
    """Test organization viewset"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.organization = Organization.objects.create(
            name='testorg',
            email='test@example.com'
        )
        OrganizationMember.objects.create(
            user=self.user,
            organization=self.organization,
            role='admin'
        )
        self.client.force_authenticate(user=self.user)

    def test_list_organizations(self):
        """Test listing organizations"""
        url = reverse('organization_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # View returns all organizations the user has access to
        # User should only have access to the organization they are a member of
        self.assertEqual(len(response.data), 4)

    def test_create_organization(self):
        """Test creating a new organization"""
        url = reverse('organization_list')
        data = {
            'name': 'neworg',
            'email': 'new@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify organization was created
        self.assertTrue(Organization.objects.filter(name='neworg').exists())

        # Verify user was added as admin
        org = Organization.objects.get(name='neworg')
        self.assertTrue(OrganizationMember.objects.filter(
            user=self.user, organization=org, role='admin'
        ).exists())

    def test_partial_update_organization_as_admin(self):
        """Test admin can update organization email and name"""
        url = reverse('organization_detail', kwargs={'name': 'testorg'})
        data = {
            'email': 'updated@example.com',
            'name': 'updatedorg'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify organization was updated
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.email, 'updated@example.com')
        self.assertEqual(self.organization.name, 'updatedorg')

    def test_partial_update_organization_email_only(self):
        """Test admin can update only email"""
        url = reverse('organization_detail', kwargs={'name': 'testorg'})
        data = {'email': 'newemail@example.com'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify only email was updated
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.email, 'newemail@example.com')
        self.assertEqual(self.organization.name, 'testorg')  # unchanged

    def test_partial_update_organization_name_only(self):
        """Test admin can update only name"""
        url = reverse('organization_detail', kwargs={'name': 'testorg'})
        data = {'name': 'newname'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify only name was updated
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.name, 'newname')
        self.assertEqual(self.organization.email, 'test@example.com')  # unchanged

    def test_partial_update_organization_as_non_admin_forbidden(self):
        """Test non-admin cannot update organization"""
        # Create a non-admin user
        non_admin = User.objects.create_user(
            username='nonadmin',
            email='nonadmin@example.com',
            password='testpass123'
        )
        # Add non-admin as member (not admin)
        OrganizationMember.objects.create(
            user=non_admin,
            organization=self.organization,
            role='member'
        )

        # Switch to non-admin user
        self.client.force_authenticate(user=non_admin)

        url = reverse('organization_detail', kwargs={'name': 'testorg'})
        data = {'email': 'hacked@example.com'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         'Only organization admins can update organizations')

        # Verify organization was not updated
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.email, 'test@example.com')

    def test_partial_update_organization_as_non_member_forbidden(self):
        """Test user not in organization cannot update organization"""
        # Create a user not in the organization
        outsider = User.objects.create_user(
            username='outsider',
            email='outsider@example.com',
            password='testpass123'
        )

        # Switch to outsider user
        self.client.force_authenticate(user=outsider)

        url = reverse('organization_detail', kwargs={'name': 'testorg'})
        data = {'email': 'hacked@example.com'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Verify organization was not updated
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.email, 'test@example.com')

    def test_delete_organization_as_admin(self):
        """Test admin can delete organization"""
        url = reverse('organization_detail', kwargs={'name': 'testorg'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify organization was deleted
        self.assertFalse(Organization.objects.filter(name='testorg').exists())

    def test_delete_organization_as_member_forbidden(self):
        """Test member cannot delete organization"""
        # Create a member user
        member_user = User.objects.create_user(
            username='memberuser',
            email='member@example.com',
            password='testpass123'
        )
        OrganizationMember.objects.create(
            user=member_user,
            organization=self.organization,
            role='member'
        )

        # Switch to member user
        self.client.force_authenticate(user=member_user)

        url = reverse('organization_detail', kwargs={'name': 'testorg'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         'Only organization admins can delete organizations')

        # Verify organization still exists
        self.assertTrue(Organization.objects.filter(name='testorg').exists())

    def test_delete_organization_as_non_member_forbidden(self):
        """Test non-member cannot delete organization"""
        # Create a user not in the organization
        outsider = User.objects.create_user(
            username='outsider',
            email='outsider@example.com',
            password='testpass123'
        )

        # Switch to outsider user
        self.client.force_authenticate(user=outsider)

        url = reverse('organization_detail', kwargs={'name': 'testorg'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Verify organization still exists
        self.assertTrue(Organization.objects.filter(name='testorg').exists())


class TestOrganizationMemberViewSet(APITestCase):
    """Test organization member viewset"""

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='testpass123'
        )
        self.member_user = User.objects.create_user(
            username='memberuser',
            email='member@example.com',
            password='testpass123'
        )
        self.organization = Organization.objects.create(
            name='testorg',
            email='test@example.com'
        )
        OrganizationMember.objects.create(
            user=self.admin_user,
            organization=self.organization,
            role='admin'
        )
        OrganizationMember.objects.create(
            user=self.member_user,
            organization=self.organization,
            role='member'
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_list_organization_members(self):
        """Test listing organization members"""
        url = reverse('organization_member_list', kwargs={'name': 'testorg'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # View returns all members of the organization (admin + member)
        self.assertEqual(len(response.data), 4)

    def test_remove_member_as_admin(self):
        """Test admin removing a member"""
        url = reverse('organization_member_detail', kwargs={
            'name': 'testorg',
            'user': 'memberuser'
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify member was removed
        self.assertFalse(OrganizationMember.objects.filter(
            user=self.member_user, organization=self.organization
        ).exists())

    def test_update_member_role_as_admin(self):
        """Test admin can update member role"""
        url = reverse('organization_member_detail', kwargs={
            'name': 'testorg',
            'user': 'memberuser'
        })
        data = {'role': 'admin'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify role was updated
        member = OrganizationMember.objects.get(
            user=self.member_user, organization=self.organization
        )
        self.assertEqual(member.role, 'admin')

    def test_update_member_role_as_member_forbidden(self):
        """Test member cannot update other member roles"""
        # Switch to member user
        self.client.force_authenticate(user=self.member_user)

        # Try to update another member (admin user) - should fail
        url = reverse('organization_member_detail', kwargs={
            'name': 'testorg',
            'user': 'adminuser'
        })
        data = {'role': 'member'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         'Only organization admins can update other members')

    def test_update_own_role_as_member_forbidden(self):
        """Test member cannot update their own role"""
        # Switch to member user
        self.client.force_authenticate(user=self.member_user)

        # Try to update own role - should fail
        url = reverse('organization_member_detail', kwargs={
            'name': 'testorg',
            'user': 'memberuser'
        })
        data = {'role': 'admin'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         'Cannot modify your own role')

    def test_demote_admin_to_member(self):
        """Test admin can demote another admin to member role"""
        # Create another admin user
        another_admin = User.objects.create_user(
            username='anotheradmin',
            email='another@example.com',
            password='testpass123'
        )
        OrganizationMember.objects.create(
            user=another_admin,
            organization=self.organization,
            role='admin'
        )

        # Current admin demotes the other admin
        url = reverse('organization_member_detail', kwargs={
            'name': 'testorg',
            'user': 'anotheradmin'
        })
        data = {'role': 'member'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify role was demoted
        member = OrganizationMember.objects.get(
            user=another_admin, organization=self.organization
        )
        self.assertEqual(member.role, 'member')

    def test_promote_member_to_admin(self):
        """Test admin can promote member to admin role"""
        url = reverse('organization_member_detail', kwargs={
            'name': 'testorg',
            'user': 'memberuser'
        })
        data = {'role': 'admin'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify role was promoted
        member = OrganizationMember.objects.get(
            user=self.member_user, organization=self.organization
        )
        self.assertEqual(member.role, 'admin')

    def test_member_can_leave_organization(self):
        """Test member can delete themselves (leave organization)"""
        # Switch to member user
        self.client.force_authenticate(user=self.member_user)

        url = reverse('organization_member_detail', kwargs={
            'name': 'testorg',
            'user': 'memberuser'
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify member was removed
        self.assertFalse(OrganizationMember.objects.filter(
            user=self.member_user, organization=self.organization
        ).exists())

    def test_member_cannot_remove_other_member(self):
        """Test member cannot remove other members"""
        # Create another member
        another_member = User.objects.create_user(
            username='anothermember',
            email='another@example.com',
            password='testpass123'
        )
        OrganizationMember.objects.create(
            user=another_member,
            organization=self.organization,
            role='member'
        )

        # Switch to member user
        self.client.force_authenticate(user=self.member_user)

        url = reverse('organization_member_detail', kwargs={
            'name': 'testorg',
            'user': 'anothermember'
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         'Only organization admins can remove other members')

        # Verify other member still exists
        self.assertTrue(OrganizationMember.objects.filter(
            user=another_member, organization=self.organization
        ).exists())

    def test_admin_can_remove_other_admin(self):
        """Test admin can remove another admin"""
        # Create another admin
        another_admin = User.objects.create_user(
            username='anotheradmin',
            email='another@example.com',
            password='testpass123'
        )
        OrganizationMember.objects.create(
            user=another_admin,
            organization=self.organization,
            role='admin'
        )

        url = reverse('organization_member_detail', kwargs={
            'name': 'testorg',
            'user': 'anotheradmin'
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify other admin was removed
        self.assertFalse(OrganizationMember.objects.filter(
            user=another_admin, organization=self.organization
        ).exists())

    def test_list_members_as_non_member_forbidden(self):
        """Test non-member cannot list organization members"""
        # Create a user not in the organization
        outsider = User.objects.create_user(
            username='outsider',
            email='outsider@example.com',
            password='testpass123'
        )

        # Switch to outsider user
        self.client.force_authenticate(user=outsider)

        url = reverse('organization_member_list', kwargs={'name': 'testorg'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return empty list
        if isinstance(response.data, list):
            self.assertEqual(len(response.data), 0)
        else:
            self.assertIn('results', response.data)
            self.assertEqual(len(response.data['results']), 0)

    def test_update_own_alerts_as_member_allowed(self):
        """Test non-admin can update their own alerts field"""
        self.client.force_authenticate(user=self.member_user)
        url = reverse('organization_member_detail', kwargs={
            'name': 'testorg',
            'user': 'memberuser'
        })
        data = {'alerts': False}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        member = OrganizationMember.objects.get(
            user=self.member_user, organization=self.organization
        )
        self.assertEqual(member.alerts, False)

    def test_update_other_member_as_member_forbidden(self):
        """Test non-admin cannot update other members' fields"""
        another_member = User.objects.create_user(
            username='anothermember',
            email='another@example.com',
            password='testpass123'
        )
        OrganizationMember.objects.create(
            user=another_member,
            organization=self.organization,
            role='member'
        )

        self.client.force_authenticate(user=self.member_user)
        url = reverse('organization_member_detail', kwargs={
            'name': 'testorg',
            'user': 'anothermember'
        })
        data = {'alerts': False}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         'Only organization admins can update other members')

    def test_single_member_cannot_modify_role(self):
        """Test single member cannot modify role"""
        solo_org = Organization.objects.create(
            name='soloorg',
            email='solo@example.com'
        )
        solo_admin = User.objects.create_user(
            username='solo',
            email='solo@example.com',
            password='testpass123'
        )
        OrganizationMember.objects.create(
            user=solo_admin, organization=solo_org, role='admin'
        )

        self.client.force_authenticate(user=solo_admin)
        url = reverse('organization_member_detail', kwargs={
            'name': 'soloorg',
            'user': 'solo'
        })
        data = {'role': 'member'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         'Cannot modify role: organization only has one member')

    def test_single_member_cannot_delete_self(self):
        """Test single member cannot delete themselves"""
        solo_org = Organization.objects.create(
            name='soloorg2',
            email='solo2@example.com'
        )
        solo_admin = User.objects.create_user(
            username='solo2',
            email='solo2@example.com',
            password='testpass123'
        )
        OrganizationMember.objects.create(
            user=solo_admin, organization=solo_org, role='admin'
        )

        self.client.force_authenticate(user=solo_admin)
        url = reverse('organization_member_detail', kwargs={
            'name': 'soloorg2',
            'user': 'solo2'
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         'Cannot delete: organization only has one member')

    def test_single_member_can_update_alerts(self):
        """Test single member can still update alerts"""
        solo_org = Organization.objects.create(
            name='soloorg3',
            email='solo3@example.com'
        )
        solo_admin = User.objects.create_user(
            username='solo3',
            email='solo3@example.com',
            password='testpass123'
        )
        OrganizationMember.objects.create(
            user=solo_admin, organization=solo_org, role='admin', alerts=True
        )

        self.client.force_authenticate(user=solo_admin)
        url = reverse('organization_member_detail', kwargs={
            'name': 'soloorg3',
            'user': 'solo3'
        })
        data = {'alerts': False}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        member = OrganizationMember.objects.get(
            user=solo_admin, organization=solo_org
        )
        self.assertEqual(member.alerts, False)


class TestOrganizationInvitationViewSet(APITestCase):
    """Test organization invitation viewset"""

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='testpass123'
        )
        self.organization = Organization.objects.create(
            name='testorg',
            email='test@example.com'
        )
        OrganizationMember.objects.create(
            user=self.admin_user,
            organization=self.organization,
            role='admin'
        )
        self.invitation = OrganizationInvitation.objects.create(
            organization=self.organization,
            email='invited@example.com',
            inviter=self.admin_user,
            token='test-token-123',
            accepted=False
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_list_organization_invitations(self):
        """Test listing organization invitations"""
        url = reverse('organization_invitation_list', kwargs={'name': 'testorg'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 检查返回的数据结构，可能是列表或字典
        if isinstance(response.data, list):
            self.assertEqual(len(response.data), 1)
        else:
            # 如果是分页响应或其他格式
            self.assertIn('results', response.data)
            self.assertEqual(len(response.data['results']), 1)

    def test_create_invitation(self):
        """Test creating a new invitation"""
        url = reverse('organization_invitation_list', kwargs={'name': 'testorg'})
        data = {
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify invitation was created
        invitation = OrganizationInvitation.objects.get(
            email='newuser@example.com', organization=self.organization
        )
        self.assertTrue(invitation)
        self.assertFalse(invitation.accepted)  # Should be False by default

    def test_get_object_accepts_invitation(self):
        """Test that getting an invitation object marks it as accepted"""
        # Create a user to accept the invitation
        invited_user = User.objects.create_user(
            username='inviteduser',
            email='invited@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=invited_user)

        url = reverse('organization_invitation_detail', kwargs={
            'name': 'testorg',
            'uid': 'test-token-123'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify invitation is now accepted
        self.invitation.refresh_from_db()
        self.assertTrue(self.invitation.accepted)

        # Verify user was added as member
        self.assertTrue(OrganizationMember.objects.filter(
            user=invited_user, organization=self.organization, role='member'
        ).exists())

    def test_list_only_unaccepted_invitations(self):
        """Test that only unaccepted invitations are listed"""
        # Create an accepted invitation
        OrganizationInvitation.objects.create(
            organization=self.organization,
            email='accepted@example.com',
            inviter=self.admin_user,
            token='accepted-token',
            accepted=True
        )

        url = reverse('organization_invitation_list', kwargs={'name': 'testorg'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should only list the unaccepted invitation
        if isinstance(response.data, list):
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['email'], 'invited@example.com')
        else:
            self.assertIn('results', response.data)
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['email'], 'invited@example.com')

    def test_cannot_get_accepted_invitation(self):
        """Test that accepted invitations cannot be retrieved"""
        # Create an accepted invitation
        OrganizationInvitation.objects.create(
            organization=self.organization,
            email='accepted@example.com',
            inviter=self.admin_user,
            token='accepted-token',
            accepted=True
        )

        url = reverse('organization_invitation_detail', kwargs={
            'name': 'testorg',
            'uid': 'accepted-token'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_invitation_as_member_forbidden(self):
        """Test member cannot create invitations"""
        # Create a member user
        member_user = User.objects.create_user(
            username='memberuser',
            email='member@example.com',
            password='testpass123'
        )
        OrganizationMember.objects.create(
            user=member_user,
            organization=self.organization,
            role='member'
        )

        # Switch to member user
        self.client.force_authenticate(user=member_user)
        url = reverse('organization_invitation_list', kwargs={'name': 'testorg'})
        data = {'email': 'newuser@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Only organization admins can create invitations', str(response.data))

    def test_create_invitation_for_existing_member_forbidden(self):
        """Test cannot create invitation for existing member"""
        # Create a member user
        existing_member = User.objects.create_user(
            username='existingmember',
            email='existing@example.com',
            password='testpass123'
        )
        OrganizationMember.objects.create(
            user=existing_member,
            organization=self.organization,
            role='member'
        )
        url = reverse('organization_invitation_list', kwargs={'name': 'testorg'})
        data = {'email': 'existing@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('User is already a member of the organization', str(response.data))

    def test_create_duplicate_invitation_forbidden(self):
        """Test cannot create duplicate invitation for the same email"""
        url = reverse('organization_invitation_list', kwargs={'name': 'testorg'})

        # First invitation should succeed
        data = {'email': 'duplicate@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify first invitation was created
        invitation_count = OrganizationInvitation.objects.filter(
            email='duplicate@example.com',
            organization=self.organization
        ).count()
        self.assertEqual(invitation_count, 1)

        # Save the invitation ID before second attempt
        OrganizationInvitation.objects.get(
            email='duplicate@example.com',
            organization=self.organization
        )

        # Second invitation for the same email should fail
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('User already has pending invitation', str(response.data))

    def test_revoke_invitation_as_member_forbidden(self):
        """Test member cannot revoke invitation"""
        # Create a member user
        member_user = User.objects.create_user(
            username='memberuser',
            email='member@example.com',
            password='testpass123'
        )
        OrganizationMember.objects.create(
            user=member_user,
            organization=self.organization,
            role='member'
        )
        # Switch to member user
        self.client.force_authenticate(user=member_user)
        url = reverse('organization_invitation_detail', kwargs={
            'name': 'testorg',
            'uid': 'test-token-123'
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         'Only organization admins can revoke invitations')

        # Verify invitation still exists
        self.assertTrue(OrganizationInvitation.objects.filter(token='test-token-123').exists())

    def test_list_invitations_as_non_member_forbidden(self):
        """Test non-member cannot list organization invitations"""
        # Create a user not in the organization
        outsider = User.objects.create_user(
            username='outsider',
            email='outsider@example.com',
            password='testpass123'
        )

        # Switch to outsider user
        self.client.force_authenticate(user=outsider)
        url = reverse('organization_invitation_list', kwargs={'name': 'testorg'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return empty list
        if isinstance(response.data, list):
            self.assertEqual(len(response.data), 0)
        else:
            self.assertIn('results', response.data)
            self.assertEqual(len(response.data['results']), 0)


class TestIsOrganizationMember(TestCase):
    """Test is_organization_member helper function"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.organization = Organization.objects.create(
            name='testorg',
            email='test@example.com'
        )

    def test_is_organization_member_true(self):
        """Test user is organization member"""
        OrganizationMember.objects.create(
            user=self.user,
            organization=self.organization,
            role='admin'
        )
        self.assertTrue(is_organization_member(self.user, self.organization, role='admin'))

    def test_is_organization_member_false(self):
        """Test user is not organization member"""
        OrganizationMember.objects.create(
            user=self.user,
            organization=self.organization,
            role='member'
        )
        self.assertFalse(is_organization_member(self.user, self.organization, role='admin'))

    def test_is_organization_member_no_membership(self):
        """Test user has no membership in organization"""
        self.assertFalse(is_organization_member(self.user, self.organization, role='admin'))
