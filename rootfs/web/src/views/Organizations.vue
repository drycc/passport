<!-- 组织管理页面 -->
<template>
    <div :id="'vue-content-' + Math.random().toString(36).substring(2)">
        <nav-bar />
        <div class="main-panel relative mt5">
            <div class="main-content">
                <main-nav :is-organizations-active="true" />

                <!-- Loading state -->
                <div
                    v-if="loading && organizations.length === 0"
                    class="w-100 mt4 ml2 mb4 mr2 limit-width"
                >
                    <el-skeleton :rows="3" animated />
                </div>

                <!-- Empty state -->
                <div
                    v-else-if="!loading && organizations.length === 0"
                    class="w-100 mt4 ml2 mb4 mr2 limit-width"
                >
                    <el-empty description="No organizations found">
                        <el-button
                            type="primary"
                            @click="handleCreateOrganizationDialog"
                        >
                            <el-icon><Plus /></el-icon>
                            Create Organization
                        </el-button>
                    </el-empty>
                </div>

                <!-- 成员列表 -->
                <div v-else class="w-100 mt4 ml2 mb4 mr2 limit-width">
                    <div class="flex justify-between items-center mb3">
                        <div>
                            <div class="flex justify-between items-center">
                                <el-dropdown v-if="organizations.length > 0">
                                    <el-button plain>
                                        {{
                                            selectedOrganization.name ||
                                            "Select Organization"
                                        }}<el-icon class="el-icon--right"
                                            ><arrow-down
                                        /></el-icon>
                                    </el-button>
                                    <template #dropdown>
                                        <el-dropdown-menu>
                                            <el-dropdown-item
                                                v-for="org in organizations"
                                                :key="org.name"
                                                @click="
                                                    handleOrganizationChange(
                                                        org,
                                                    )
                                                "
                                                >{{
                                                    org.name
                                                }}</el-dropdown-item
                                            >
                                            <el-dropdown-item
                                                :icon="Plus"
                                                divided
                                                @click="
                                                    handleCreateOrganizationDialog
                                                "
                                                >Create new
                                                organization</el-dropdown-item
                                            >
                                        </el-dropdown-menu>
                                    </template>
                                </el-dropdown>
                                <div
                                    class="fl ml2"
                                    v-if="selectedOrganization.name"
                                >
                                    <el-tooltip
                                        :content="
                                            getTooltipMessage(
                                                'editOrganization',
                                            )
                                        "
                                        :disabled="canEditOrganization()"
                                    >
                                        <el-button
                                            type="primary"
                                            :icon="Edit"
                                            @click="
                                                handleEditOrganizationDialog
                                            "
                                            :disabled="!canEditOrganization()"
                                            circle
                                        />
                                    </el-tooltip>
                                    <el-tooltip
                                        :content="
                                            getTooltipMessage(
                                                'deleteOrganization',
                                            )
                                        "
                                        :disabled="canDeleteOrganization()"
                                    >
                                        <el-button
                                            type="danger"
                                            :icon="Delete"
                                            @click="handleDeleteOrganization"
                                            :disabled="!canDeleteOrganization()"
                                            circle
                                        />
                                    </el-tooltip>
                                </div>
                            </div>
                        </div>
                        <el-tooltip
                            :content="getTooltipMessage('inviteMember')"
                            :disabled="canInviteMember()"
                        >
                            <el-button
                                v-if="selectedOrganization.name"
                                type="primary"
                                @click="inviteDialog.showModal = true"
                                :disabled="!canInviteMember()"
                                >Invite member</el-button
                            >
                        </el-tooltip>
                    </div>
                    <el-divider v-if="selectedOrganization.name" />
                    <el-table
                        v-if="selectedOrganization.name"
                        :data="selectedOrganization.members"
                        style="width: 100%"
                        v-loading="loading"
                    >
                        <el-table-column prop="user" label="Member">
                            <template #default="scope">
                                <div class="flex items-center">
                                    <el-avatar
                                        class="avatar mr2"
                                        :size="48"
                                        :src="`/user/avatar/${scope.row.user}/`"
                                    />
                                    <div>
                                        {{ scope.row.user }}
                                    </div>
                                </div>
                            </template>
                        </el-table-column>
                        <el-table-column prop="email" label="Email" />
                        <el-table-column label="Authentication">
                            <template #default="scope">
                                <img
                                    class="mr2"
                                    src="../../src/assets/icons/github.svg"
                                />
                                <img
                                    class="mr2"
                                    src="../../src/assets/icons/google.svg"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column label="Alerts">
                            <template #default="scope">
                                <el-tooltip
                                    :content="getTooltipMessage('editAlerts')"
                                    :disabled="canEditMember(scope.row)"
                                >
                                    <el-switch
                                        v-model="scope.row.alerts"
                                        size="small"
                                        :disabled="!canEditMember(scope.row)"
                                        @change="
                                            (newAlerts) =>
                                                handleMemberAlertsChange(
                                                    scope.row,
                                                    newAlerts,
                                                )
                                        "
                                    />
                                </el-tooltip>
                            </template>
                        </el-table-column>
                        <el-table-column label="Role">
                            <template #default="scope">
                                <el-tooltip
                                    :content="getTooltipMessage('changeRole')"
                                    :disabled="canEditMemberRole(scope.row)"
                                >
                                    <el-select
                                        v-model="scope.row.role"
                                        @change="
                                            (newRole) =>
                                                handleMemberRoleChange(
                                                    scope.row,
                                                    newRole,
                                                )
                                        "
                                        size="small"
                                        :disabled="
                                            !canEditMemberRole(scope.row)
                                        "
                                    >
                                        <el-option
                                            v-for="roleOption in roleOptions"
                                            :key="roleOption.value"
                                            :label="roleOption.label"
                                            :value="roleOption.value"
                                        />
                                    </el-select>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                        <el-table-column align="right">
                            <template #default="scope">
                                <el-tooltip
                                    :content="getTooltipMessage('removeMember')"
                                    :disabled="canRemoveMember(scope.row)"
                                >
                                    <el-button
                                        type="danger"
                                        plain
                                        @click="handleRemoveMember(scope.row)"
                                        :disabled="!canRemoveMember(scope.row)"
                                        >Remove</el-button
                                    >
                                </el-tooltip>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>

                <!-- 邀请列表 -->
                <div
                    class="w-100 mt4 ml2 mb4 mr2 limit-width"
                    v-if="
                        selectedOrganization.name &&
                        selectedOrganization.invitations.length > 0
                    "
                >
                    <h2 class="f4 b mb3 gray">Invitations</h2>

                    <el-table
                        :data="selectedOrganization.invitations"
                        style="width: 100%"
                        v-loading="loading"
                    >
                        <el-table-column prop="email" label="Email" />
                        <el-table-column prop="inviter" label="Inviter" />
                        <el-table-column prop="created" label="Created" />
                        <el-table-column align="right">
                            <template #default="scope">
                                <el-tooltip
                                    :content="
                                        getTooltipMessage('revokeInvitation')
                                    "
                                    :disabled="canRevokeInvitation()"
                                >
                                    <el-button
                                        type="danger"
                                        plain
                                        @click="
                                            handleRevokeInvitation(scope.row)
                                        "
                                        :disabled="!canRevokeInvitation()"
                                        >Revoke</el-button
                                    >
                                </el-tooltip>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>

                <!-- invite modal dialog -->
                <el-dialog
                    v-model="inviteDialog.showModal"
                    title="Invite someone to join your organization"
                >
                    <div class="mb4">
                        <label class="db fw6 mb2 gray" for="email"
                            >Email address</label
                        >
                        <el-input
                            v-model="inviteDialog.email"
                            type="email"
                            id="email"
                            placeholder="Enter email address"
                        />
                    </div>
                    <template #footer>
                        <span class="dialog-footer">
                            <el-button @click="inviteDialog.showModal = false"
                                >Cancel</el-button
                            >
                            <el-button type="primary" @click="handleSendInvite">
                                Send invite
                            </el-button>
                        </span>
                    </template>
                </el-dialog>

                <!-- create organization modal dialog -->
                <el-dialog
                    v-model="createOrganizationDialog.showModal"
                    title="Create new organization"
                >
                    <div class="mb4">
                        <label class="db fw6 mb2 gray" for="name"
                            >Organization name</label
                        >
                        <el-input
                            v-model="createOrganizationDialog.name"
                            type="text"
                            placeholder="Organization name"
                        />
                    </div>
                    <div class="mb4">
                        <label class="db fw6 mb2 gray" for="email"
                            >Email address</label
                        >
                        <el-input
                            v-model="createOrganizationDialog.email"
                            type="email"
                            placeholder="Enter email address"
                        />
                    </div>
                    <template #footer>
                        <span class="dialog-footer">
                            <el-button
                                @click="
                                    createOrganizationDialog.showModal = false
                                "
                                >Cancel</el-button
                            >
                            <el-button
                                type="primary"
                                @click="handleCreateOrganization"
                            >
                                Create organization
                            </el-button>
                        </span>
                    </template>
                </el-dialog>

                <!-- edit organization modal dialog -->
                <el-dialog
                    v-model="editOrganizationDialog.showModal"
                    title="Edit organization"
                >
                    <div class="mb4">
                        <label class="db fw6 mb2 gray" for="name"
                            >Organization name</label
                        >
                        <el-input
                            v-model="editOrganizationDialog.name"
                            type="text"
                            placeholder="Organization name"
                        />
                    </div>
                    <div class="mb4">
                        <label class="db fw6 mb2 gray" for="email"
                            >Email address</label
                        >
                        <el-input
                            v-model="editOrganizationDialog.email"
                            type="email"
                            placeholder="Enter email address"
                        />
                    </div>
                    <template #footer>
                        <span class="dialog-footer">
                            <el-button
                                @click="
                                    editOrganizationDialog.showModal = false
                                "
                                >Cancel</el-button
                            >
                            <el-button
                                type="primary"
                                @click="handleEditOrganization"
                            >
                                Edit organization
                            </el-button>
                        </span>
                    </template>
                </el-dialog>
            </div>
        </div>
    </div>
</template>

<script>
import Organizations from "./Organizations";
export default Organizations;
</script>
