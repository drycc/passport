import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainNav from "../components/MainNav.vue";
import MainFooter from "../components/MainFooter.vue";
import { reactive, toRefs, onMounted } from "vue";
import { Plus, Edit, Delete, ArrowDown } from "@element-plus/icons-vue";
import { ElMessage, ElTooltip } from "element-plus";
import {
  getOrganizations,
  createOrganization,
  updateOrganization,
  deleteOrganization,
  getOrganizationMembers,
  getOrganizationInvitations,
  createOrganizationInvitation,
  removeOrganizationMember,
  updateOrganizationMemberRole,
  updateOrganizationMemberAlerts,
  revokeOrganizationInvitation,
  dealOrganizationList,
  dealMemberList,
  dealInvitationList,
} from "../services/organization.js";
import { getUser, dealUser } from "../services/user.js";

export default {
  name: "Organizations",
  components: {
    "nav-bar": NavBar,
    "nav-box": NavBox,
    "main-nav": MainNav,
    "main-footer": MainFooter,
    "el-tooltip": ElTooltip,
  },
  setup() {
    const state = reactive({
      loading: false,
      currentUser: "", // Current user username
      roleOptions: [
        { value: "admin", label: "Admin" },
        { value: "member", label: "Member" },
      ],
      inviteDialog: {
        email: "",
        showModal: false,
      },
      createOrganizationDialog: {
        name: "",
        email: "",
        showModal: false,
      },
      editOrganizationDialog: {
        name: "",
        email: "",
        showModal: false,
      },
      organizations: [],
      selectedOrganization: {
        name: "",
        email: "",
        members: [],
        invitations: [],
      },
    });

    // Helper functions for role-based access control
    const getCurrentUserRole = () => {
      const currentMember = state.selectedOrganization.members.find(
        member => member.user === state.currentUser
      );
      return currentMember?.role || "member";
    };

    const isCurrentUserAdmin = () => {
      return getCurrentUserRole() === "admin";
    };

    const canEditMember = (member) => {
      if (isCurrentUserAdmin()) return true;
      return member.user === state.currentUser;
    };

    const canEditMemberRole = (member) => {
      return isCurrentUserAdmin();
    };

    const canRemoveMember = (member) => {
      if (isCurrentUserAdmin()) return true;
      return member.user === state.currentUser;
    };

    const canRevokeInvitation = () => {
      return isCurrentUserAdmin();
    };

    const canInviteMember = () => {
      return isCurrentUserAdmin();
    };

    const canEditOrganization = () => {
      return isCurrentUserAdmin();
    };

    const canDeleteOrganization = () => {
      return isCurrentUserAdmin();
    };

    // Tooltip message management
    const getTooltipMessage = (action) => {
      const messages = {
        editOrganization: "Requires admin role",
        deleteOrganization: "Requires admin role",
        inviteMember: "Requires admin role",
        changeRole: "Requires admin role",
        editAlerts: "Requires admin role or your own account",
        removeMember: "Requires admin role or your own account",
        revokeInvitation: "Requires admin role"
      };
      return messages[action] || "Permission denied";
    };

    // Load current user info
    const loadCurrentUser = async () => {
      try {
        const userResponse = await getUser();
        const userData = dealUser(userResponse);
        state.currentUser = userData.username;
      } catch (error) {
        console.error('Error loading current user:', error);
      }
    };

    // Load organizations on component mount
    const loadOrganizations = async () => {
      try {
        state.loading = true;
        
        // Load current user first
        await loadCurrentUser();
        
        const response = await getOrganizations();
        state.organizations = dealOrganizationList(response);
        
        // Load first organization data if available
        if (state.organizations.length > 0) {
          const firstOrg = state.organizations[0];
          state.selectedOrganization.name = firstOrg.name;
          state.selectedOrganization.email = firstOrg.email;

          // Load members and invitations in parallel
          const [membersResponse, invitationsResponse] = await Promise.all([
            getOrganizationMembers(firstOrg.name),
            getOrganizationInvitations(firstOrg.name)
          ]);

          state.selectedOrganization.members = dealMemberList(membersResponse);
          state.selectedOrganization.invitations = dealInvitationList(invitationsResponse);
        }
      } catch (error) {
        ElMessage.error('Failed to load organizations');
        console.error('Error loading organizations:', error);
      } finally {
        state.loading = false;
      }
    };

    // Load organization members and invitations
    const loadOrganizationData = async (org) => {
      try {
        state.selectedOrganization.name = org.name;
        state.selectedOrganization.email = org.email;

        // Load members and invitations in parallel
        const [membersResponse, invitationsResponse] = await Promise.all([
          getOrganizationMembers(org.name),
          getOrganizationInvitations(org.name)
        ]);

        state.selectedOrganization.members = dealMemberList(membersResponse);
        state.selectedOrganization.invitations = dealInvitationList(invitationsResponse);
      } catch (error) {
        ElMessage.error('Failed to load organization data');
        console.error('Error loading organization data:', error);
      }
    };

    const handleSendInvite = async () => {
      try {
        if (!state.inviteDialog.email) {
          ElMessage.warning('Please enter an email address');
          return;
        }
        
        await createOrganizationInvitation(state.selectedOrganization.name, state.inviteDialog.email);
        ElMessage.success('Invitation sent successfully');
        
        // Reload invitations
        await loadOrganizationData({ name: state.selectedOrganization.name, email: state.selectedOrganization.email });
        
        // Reset dialog
        state.inviteDialog.showModal = false;
        state.inviteDialog.email = '';
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || 'Failed to send invitation');
        console.error('Error sending invitation:', error);
      }
    };

    const handleCreateOrganization = async () => {
      try {
        if (!state.createOrganizationDialog.name || !state.createOrganizationDialog.email) {
          ElMessage.warning('Please fill in all fields');
          return;
        }
        
        await createOrganization({
          name: state.createOrganizationDialog.name,
          email: state.createOrganizationDialog.email
        });
        
        ElMessage.success('Organization created successfully');
        
        // Reload organizations
        await loadOrganizations();
        
        // Reset dialog
        state.createOrganizationDialog.showModal = false;
        state.createOrganizationDialog.name = '';
        state.createOrganizationDialog.email = '';
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || 'Failed to create organization');
        console.error('Error creating organization:', error);
      }
    };

    const handleEditOrganization = async () => {
      try {
        await updateOrganization(state.selectedOrganization.name, {
          name: state.editOrganizationDialog.name,
          email: state.editOrganizationDialog.email
        });

        ElMessage.success('Organization updated successfully');

        const newName = state.editOrganizationDialog.name;
        const newEmail = state.editOrganizationDialog.email;
        const oldName = state.selectedOrganization.name;

        // Reload organizations to get updated list
        await loadOrganizations();

        // If name changed, reload organization data with new name
        if (oldName !== newName) {
          const updatedOrg = state.organizations.find(org => org.name === newName);
          if (updatedOrg) {
            await loadOrganizationData(updatedOrg);
          }
        } else {
          // Update selectedOrganization directly if name didn't change
          state.selectedOrganization.email = newEmail;
        }

        // Close dialog and reset
        state.editOrganizationDialog.showModal = false;
        state.editOrganizationDialog.name = '';
        state.editOrganizationDialog.email = '';
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || 'Failed to update organization');
        console.error('Error updating organization:', error);
      }
    };

    const handleDeleteOrganization = async () => {
      try {
        await deleteOrganization(state.selectedOrganization.name);
        ElMessage.success('Organization deleted successfully');
        
        // Reload organizations
        await loadOrganizations();
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || 'Failed to delete organization');
        console.error('Error deleting organization:', error);
      }
    };

    const handleOrganizationChange = async (org) => {
      await loadOrganizationData(org);
    };

    const handleCreateOrganizationDialog = () => {
      state.createOrganizationDialog.showModal = true;
    };

    const handleEditOrganizationDialog = () => {
      state.editOrganizationDialog.name = state.selectedOrganization.name;
      state.editOrganizationDialog.email = state.selectedOrganization.email;
      state.editOrganizationDialog.showModal = true;
    };

    const handleMemberRoleChange = async (member, newRole) => {
      try {
        await updateOrganizationMemberRole(state.selectedOrganization.name, member.user, newRole);
        ElMessage.success('Member role updated successfully');
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || 'Failed to update member role');
        console.error('Error updating member role:', error);
        
        // Reload members to revert the change
        await loadOrganizationData({ name: state.selectedOrganization.name, email: state.selectedOrganization.email });
      }
    };

    const handleMemberAlertsChange = async (member, newAlerts) => {
      try {
        await updateOrganizationMemberAlerts(state.selectedOrganization.name, member.user, newAlerts);
        ElMessage.success('Member alerts updated successfully');
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || 'Failed to update member alerts');
        console.error('Error updating member alerts:', error);
        
        // Reload members to revert the change
        await loadOrganizationData({ name: state.selectedOrganization.name, email: state.selectedOrganization.email });
      }
    };

    const handleRemoveMember = async (member) => {
      try {
        await removeOrganizationMember(state.selectedOrganization.name, member.user);
        ElMessage.success('Member removed successfully');
        
        // Reload members
        await loadOrganizationData({ name: state.selectedOrganization.name, email: state.selectedOrganization.email });
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || 'Failed to remove member');
        console.error('Error removing member:', error);
      }
    };

    const handleRevokeInvitation = async (invitation) => {
      try {
        await revokeOrganizationInvitation(state.selectedOrganization.name, invitation.token);
        ElMessage.success('Invitation revoked successfully');
        
        // Reload invitations
        await loadOrganizationData({ name: state.selectedOrganization.name, email: state.selectedOrganization.email });
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || 'Failed to revoke invitation');
        console.error('Error revoking invitation:', error);
      }
    };

    // Lifecycle hook
    onMounted(() => {
      loadOrganizations();
    });

    return {
      ...toRefs(state),
      Plus,
      Edit,
      Delete,
      ArrowDown,
      handleSendInvite,
      handleCreateOrganization,
      handleCreateOrganizationDialog,
      handleEditOrganizationDialog,
      handleEditOrganization,
      handleDeleteOrganization,
      handleOrganizationChange,
      handleMemberRoleChange,
      handleMemberAlertsChange,
      handleRemoveMember,
      handleRevokeInvitation,
      getCurrentUserRole,
      isCurrentUserAdmin,
      canEditMember,
      canEditMemberRole,
      canRemoveMember,
      canRevokeInvitation,
      canInviteMember,
      canEditOrganization,
      canDeleteOrganization,
      getTooltipMessage,
    };
  },
};
