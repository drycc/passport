<!--app列表页-->
<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar :user="user" />
    <div class="main-panel ui-page-shell">
        <div class="main-content">
            <main-nav :is-account-setting-active="true"/>
        <ul class="ui-settings-list">
            <li class="ui-settings-card">
                <div class="ui-settings-section">
                    <div class="ui-settings-head">
                        <div class="ui-settings-title" role="heading" aria-level="3">
                            Profile
                        </div>
                        <div class="ui-settings-desc">
                            Your username is your identity on drycc and is used to log in, update account may require email confirmation.
                        </div>
                    </div>

                    <div class="ui-settings-body">
                        <div class="ui-avatar-placeholder">
                        </div>
                        <div class="ui-settings-content-wrap">
                            <div class="ui-form-grid">
                                <div>
                                    <div>
                                        <label class="ui-field-label" for="name">Username
                                        </label>
                                        <div class="ui-inline-field">
                                            <input autocomplete="off" placeholder="Your name"  id="username" :value=user.username
                                                    class="ui-input"
                                                    disabled="disabled"
                                                    type="text">
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <div>
                                        <form role="form">
                                            <label class="ui-field-label"
                                                   for="new-e-mail">Email
                                                Address</label>
                                            <div class="ui-inline-field">
                                                <input autocomplete="off" placeholder="Your email address" @input="emailInputChange($event)"  id="new-e-mail" :value=user.email
                                                       class="ui-input"
                                                       type="text">

                                                <div :class=emailBTN>
                                                    <button class="ui-btn ui-btn--primary" @click="submitEmail()"
                                                            type="button"> Save
                                                    </button>
                                                    <button class="ui-btn ui-btn--secondary" @click="cancelEmail()"
                                                            type="button"> Cancel
                                                    </button>
                                                </div>
                                            </div>
                                            <div style="display: none" class="email_error">提示信息</div>
                                        </form>
                                    </div>
                                    <span class="confirmable-action"> </span>
                                </div>
                                <div>
                                    <div>
                                        <form role="form">
                                            <label class="ui-field-label" for="name">Last Name
                                            </label>
                                            <div class="ui-inline-field">
                                                <input autocomplete="off" placeholder="Your last name" @input="lastNameInputChange($event)" id="last-name" :value=user.last_name
                                                       class="ui-input"
                                                       type="text">
                                                <div :class=lastNameBTN>
                                                    <button
                                                            class="ui-btn ui-btn--primary" @click="submitLastName()"
                                                            type="button"> Save
                                                    </button>
                                                    <button
                                                            class="ui-btn ui-btn--secondary" @click="cancelLastName()"
                                                            type="button"> Cancel
                                                    </button>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                                <div>
                                    <div>
                                        <form role="form">
                                            <label class="ui-field-label" for="name">First Name
                                            </label>
                                            <div class="ui-inline-field">
                                                <input autocomplete="off" placeholder="Your first name" @input="firstNameInputChange($event)" id="first-name" :value=user.first_name
                                                       class="ui-input"
                                                       type="text">
                                                <div :class=firstNameBTN>
                                                    <button
                                                            class="ui-btn ui-btn--primary" @click="submitFirstName()"
                                                            type="button"> Save
                                                    </button>
                                                    <button
                                                            class="ui-btn ui-btn--secondary" @click="cancelFirstName()"
                                                            type="button"> Cancel
                                                    </button>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                                <p class="ui-settings-note">
                                Manage your avatar using <a href="https://gravatar.com" target="_blank" rel="noopener noreferrer" class="ui-inline-link">Gravatar</a>.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </li>
            <li class="ui-settings-card">
                <div class="ui-settings-section">
                    <div class="ui-settings-head">
                        <div class="ui-settings-title" role="heading" aria-level="3">
                            Password
                        </div>

                        <div class="ui-settings-desc">
                            Change the password here.
                        </div>
                    </div>

                    <div class="ui-settings-body">
                        <div>
                            <div class="ui-settings-content-wrap">
                            <div class="ui-form-grid ui-form-grid--password">
                                <form role="form" method="POST" class="ui-password-form">
                                    <div class="ui-form-group">
                                        <label for="current-password">Current Password</label>
                                        <input name="password" @input="currentPasswordChange($event)"
                                               placeholder="enter your current password"
                                               id="current-password"
                                               class="ui-input"
                                               type="password">
                                    </div>

                                    <div class="ui-form-group">
                                        <label for="new-password">New
                                            Password</label>
                                        <input placeholder="enter a new password" @input="newPasswordChange($event)"
                                               id="new-password"
                                               class="ui-input"
                                               type="password">
                                        <p class="ui-settings-note">
                                            Password must be 8 or more characters.
                                        </p>
                                    </div>

                                    <div class="ui-form-group">
                                        <label for="confirm-new-password">Confirm
                                            New Password</label>
                                        <input placeholder="enter the password again"  @input="confirmNewPasswordChange($event)"
                                               id="confirm-new-password"
                                               class="ui-input"
                                               type="password">
                                    </div>

                                    <div class="ui-form-group">
                                        <button @click="submitPassowrd()"
                                                :class=updateBTN
                                                type="button">
                                            Update Password
                                        </button>
                                    </div>
                                </form>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </li>
            <li class="ui-settings-card">
                <div class="ui-settings-section">
                    <div class="ui-settings-head">
                        <div class="ui-settings-title" role="heading" aria-level="3">
                            Linked SSO
                        </div>
                        <div class="ui-settings-desc">
                            Manage linked OAuth identities for your account.
                        </div>
                    </div>
                    <div class="ui-settings-body">
                        <div class="ui-identities-table-wrap">
                            <el-table class="ui-identities-table" :data="identities" v-loading="loading" style="width: 100%">
                                <el-table-column label="Provider">
                                    <template #default="scope">
                                        <el-space alignment="center" :size="8">
                                            <span v-html="scope.row.icon"></span>
                                            <span>{{ scope.row.display_name }}</span>
                                        </el-space>
                                    </template>
                                </el-table-column>
                                <el-table-column prop="email" label="Email" />
                                <el-table-column label="Action" width="140">
                                    <template #default="scope">
                                        <el-button type="danger" plain @click="handleUnlink(scope.row)">Unlink</el-button>
                                    </template>
                                </el-table-column>
                                <template #empty>
                                    <div class="ui-table-empty-state">
                                        <div class="ui-table-empty-state__icon" aria-hidden="true"></div>
                                        <p class="ui-table-empty-state__title">No linked identities</p>
                                        <p class="ui-table-empty-state__desc">Link an OAuth provider below to get started.</p>
                                    </div>
                                </template>
                            </el-table>
                        </div>
                    </div>
                </div>
            </li>
            <li class="ui-settings-card">
                <div class="ui-settings-section">
                    <div class="ui-settings-head">
                        <div class="ui-settings-title" role="heading" aria-level="3">
                            Link New SSO
                        </div>
                        <div class="ui-settings-desc">
                            Choose a provider to link a new OAuth identity.
                        </div>
                    </div>
                    <div class="ui-settings-body">
                        <div v-if="providers.length === 0" class="ui-left-align">
                            <el-empty description="No providers available." :image-size="80" />
                        </div>
                        <div v-else class="ui-sso-providers-wrap">
                            <el-space wrap class="ui-sso-providers-list">
                                <el-button
                                    v-for="provider in providers"
                                    :key="provider.name"
                                    type="primary"
                                    plain
                                    @click.prevent="handleLink(provider)"
                                >
                                    <span v-html="provider.icon"></span>
                                    <strong>Link {{ provider.name.charAt(0).toUpperCase() + provider.name.slice(1) }}</strong>
                                </el-button>
                            </el-space>
                        </div>
                    </div>
                </div>
            </li>
        </ul>
      </div>
  </div>
  <main-footer />
</div>
</template>
<style lang="css" scoped>
.ui-page-shell {
    padding: 14px 0 22px;
}

.ui-settings-list {
    list-style: none;
    margin: 0;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.ui-settings-card {
    border: 1px solid rgba(217, 226, 239, 0.92);
    border-radius: 14px;
    padding: 22px;
    background: linear-gradient(180deg, #ffffff 0%, #fcfdff 100%);
    box-shadow: 0 10px 22px rgba(16, 42, 72, 0.06);
}

.ui-settings-section {
    display: flex;
    gap: 24px;
}

.ui-settings-head {
    flex: 0 0 230px;
}

.ui-settings-title {
    font-size: var(--ui-font-size-5xl);
    line-height: 1.3;
    color: var(--ui-color-primary);
    font-weight: var(--ui-font-weight-bold);
    letter-spacing: -0.01em;
}

.ui-settings-desc {
    margin-top: 12px;
    color: var(--ui-color-text-secondary);
    font-size: var(--ui-font-size-xl);
    line-height: 1.35;
    max-width: 220px;
}

.ui-settings-body {
    flex: 1;
}

.ui-avatar-placeholder {
    display: none;
}

.ui-form-grid {
    max-width: 760px;
}

.ui-form-grid > div {
    margin-bottom: 14px;
}

.ui-form-grid > div:last-of-type {
    margin-bottom: 0;
}

.ui-settings-content-wrap {
    width: 100%;
    max-width: none;
    border: 1px solid var(--ui-color-border);
    border-radius: 14px;
    background: #fff;
    padding: 14px;
    box-sizing: border-box;
}

.ui-field-label {
    display: block;
    margin-bottom: 8px;
    font-weight: var(--ui-font-weight-bold);
    color: #2a3f5e;
    font-size: var(--ui-font-size-lg);
}

.ui-inline-field {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.ui-input {
    width: 100%;
    max-width: 500px;
    height: 42px;
    border: 1px solid var(--ui-color-border);
    border-radius: 10px;
    padding: 0 13px;
    color: var(--ui-color-text);
    background: #fbfcff;
    box-sizing: border-box;
    transition: all 0.16s ease;
}

.ui-input:focus {
    outline: 2px solid rgba(47, 128, 237, 0.2);
    border-color: var(--ui-color-primary);
    background: #fff;
    box-shadow: 0 6px 16px rgba(47, 128, 237, 0.16);
}

.ui-inline-actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

.is-hidden {
    display: none;
}

.ui-btn {
    border-radius: 10px;
    border: 1px solid transparent;
    height: 36px;
    padding: 0 15px;
    cursor: pointer;
    font-weight: var(--ui-font-weight-bold);
    transition: all 0.18s ease;
}

.ui-btn--primary {
    background: var(--ui-color-primary);
    border-color: var(--ui-color-primary);
    color: #fff;
}

.ui-btn--primary:hover {
    background: var(--ui-color-primary-hover);
    border-color: var(--ui-color-primary-hover);
    box-shadow: 0 8px 18px rgba(47, 128, 237, 0.28);
}

.ui-btn--secondary {
    background: #fff;
    border-color: var(--ui-color-border);
    color: var(--ui-color-text);
}

.ui-btn--secondary:hover {
    border-color: var(--ui-color-primary);
    color: var(--ui-color-primary);
}

.is-disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.ui-form-group {
    margin-bottom: 16px;
}

.ui-password-form {
    width: 100%;
}

.ui-form-grid--password .ui-form-group {
    display: block;
    margin-bottom: 14px;
}

.ui-form-grid--password .ui-form-group > label {
    display: block;
    margin-bottom: 8px;
    color: #2f3f56;
    font-weight: var(--ui-font-weight-semibold);
}

.ui-form-grid--password .ui-form-group > .ui-input {
    width: 100%;
    max-width: 500px;
}

.ui-form-grid--password .ui-form-group > .ui-settings-note {
    margin: 8px 0 0;
    font-size: var(--ui-font-size-md);
}

.ui-form-grid--password .ui-form-group > .ui-btn {
    margin-top: 4px;
}

.ui-identities-table-wrap {
    width: 100%;
    border: 1px solid var(--ui-color-border);
    border-radius: 14px;
    overflow: hidden;
    background: #fff;
    box-sizing: border-box;
}

:deep(.ui-identities-table) {
    border: none;
    border-radius: 0;
    overflow: visible;
}

:deep(.ui-identities-table .el-table__inner-wrapper),
:deep(.ui-identities-table .el-table__header-wrapper),
:deep(.ui-identities-table .el-table__body-wrapper) {
    border-radius: 0;
}

.ui-sso-providers-wrap {
    width: 100%;
    border: 1px solid var(--ui-color-border);
    border-radius: 14px;
    background: #fff;
    min-height: 92px;
    padding: 14px;
    box-sizing: border-box;
}

.ui-sso-providers-list {
    width: 100%;
}

.ui-table-empty-state {
    min-height: 120px;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    color: var(--ui-color-text-secondary);
    background: transparent;
}

.ui-table-empty-state__icon {
    width: 26px;
    height: 26px;
    border-radius: 999px;
    border: 2px solid #b9cae3;
    position: relative;
}

.ui-table-empty-state__icon::after {
    content: "";
    position: absolute;
    left: 50%;
    top: 50%;
    width: 8px;
    height: 2px;
    margin-left: -4px;
    margin-top: -1px;
    border-radius: 2px;
    background: #8fa8c9;
}

.ui-table-empty-state__title {
    margin: 0;
    font-size: var(--ui-font-size-lg);
    font-weight: var(--ui-font-weight-semibold);
    color: #4f6280;
}

.ui-table-empty-state__desc {
    margin: 0;
    font-size: var(--ui-font-size-sm);
}

:deep(.ui-identities-table .el-table__empty-block) {
    width: 100%;
    min-height: 120px;
}

:deep(.ui-identities-table .el-table__empty-text) {
    width: 100%;
    margin: 0;
    line-height: normal;
}

.ui-settings-note {
    color: var(--ui-color-text-secondary);
    margin: 10px 0 0;
    font-size: var(--ui-font-size-lg);
}

.ui-inline-link {
    color: var(--ui-color-primary);
    text-decoration: none;
}

.ui-inline-link:hover {
    color: var(--ui-color-primary-hover);
}

.ui-left-align {
    text-align: left;
}

.el-empty-custom {
    --el-empty-padding: 0px;
}

@media (max-width: 900px) {
    .ui-settings-card {
        padding: 16px;
    }

    .ui-settings-section {
        flex-direction: column;
        gap: 16px;
    }

    .ui-settings-head {
        flex: 1 1 auto;
    }

    .ui-settings-title {
        font-size: var(--ui-font-size-4xl);
    }

    .ui-settings-desc {
        font-size: var(--ui-font-size-lg);
        max-width: none;
    }

    .ui-settings-content-wrap {
        padding: 12px;
    }

    .ui-form-grid--password .ui-form-group {
        margin-bottom: 12px;
    }
}
</style>
<script>
import AccountSetting from  "./AccountSetting"
export default AccountSetting
</script>
