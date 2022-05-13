<!--app列表页-->
<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <div class="main-panel bg-lightest-silver relative mt5">
        <div class="main-content">
            <main-nav :is-account-setting-active="true"/>
        <ul class="list-group list-group-lg">
            <li class="list-group-item ember-view">
                <div class="panel-section">
                    <div class="section-description">
                        <div class="section-title f3 purple" role="heading" aria-level="3">
                            Profile
                        </div>
                        <div class="mt2 f5 lh-copy dark-gray">
                            Your username is your identity on drycc and is used to log in, update account may require email confirmation.
                        </div>
                    </div>

                    <div class="panel-content">
                        <div class="avatar">
                        </div>
                        <div class="edit-first">
                            <div class="ember-view">
                                <div class="ember-view">
                                    <label class="hk-label db mb2" for="name">Username
                                    </label>
                                    <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                        <input autocomplete="off" placeholder="Your name"  id="username" :value=user.username
                                                class="mr2 mb2 w-100 mw6 ember-text-field hk-input ember-view"
                                                disabled="disabled"
                                                type="text">
                                    </div>
                                </div>
                            </div>
                            <div class="ember-view">
                                <div class="ember-view">
                                    <form role="form">
                                        <label class="hk-label db mb2"
                                               for="new-e-mail">Email
                                            Address</label>
                                        <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                            <input autocomplete="off" placeholder="Your email address" @input="emailInputChange($event)"  id="new-e-mail" :value=user.email
                                                   class="mr2 mb2 w-100 mw6 ember-text-field hk-input ember-view"
                                                   type="text">

                                            <div :class=emailBTN data-test-target="hk-inline-buttons">
                                                <button class="mr1 async-button default hk-button--primary ember-view" @click="submitEmail()"
                                                        type="button"> Save
                                                </button>
                                                <button class="async-button default hk-button--secondary ember-view" @click="cancelEmail()"
                                                        type="button"> Cancel
                                                </button>
                                            </div>
                                        </div>
                                        <div style="display: none" class="email_error">提示信息</div>
                                    </form>
                                </div>
                                <span class="confirmable-action ember-view"> </span>
                            </div>
                            <div class="ember-view">
                                <div class="ember-view">
                                    <form role="form">
                                        <label class="hk-label db mb2" for="name">Last Name
                                        </label>
                                        <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                            <input autocomplete="off" placeholder="Your last name" @input="lastNameInputChange($event)" id="last-name" :value=user.last_name
                                                   class="mr2 mb2 w-100 mw6 ember-text-field hk-input ember-view"
                                                   type="text">
                                            <div :class=lastNameBTN data-test-target="hk-inline-buttons">
                                                <button
                                                        class="mr1 async-button default hk-button--primary ember-view" @click="submitLastName()"
                                                        type="button"> Save
                                                </button>
                                                <button
                                                        class="async-button default hk-button--secondary ember-view" @click="cancelLastName()"
                                                        type="button"> Cancel
                                                </button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                            <div class="ember-view">
                                <div class="ember-view">
                                    <form role="form">
                                        <label class="hk-label db mb2" for="name">First Name
                                        </label>
                                        <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                            <input autocomplete="off" placeholder="Your first name" @input="firstNameInputChange($event)" id="first-name" :value=user.first_name
                                                   class="mr2 mb2 w-100 mw6 ember-text-field hk-input ember-view"
                                                   type="text">
                                            <div :class=firstNameBTN data-test-target="hk-inline-buttons">
                                                <button
                                                        class="mr1 async-button default hk-button--primary ember-view" @click="submitFirstName()"
                                                        type="button"> Save
                                                </button>
                                                <button
                                                        class="async-button default hk-button--secondary ember-view" @click="cancelFirstName()"
                                                        type="button"> Cancel
                                                </button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                            <p class="f5 dark-gray">
                            Manage your avatar using <a href="https://gravatar.com" target="_blank" class="hk-link">Gravatar</a>.
                            </p>
                        </div>
                    </div>
                </div>
            </li>
            <li class="list-group-item ember-view">
                <div class="panel-section">
                    <div class="section-description">
                        <div class="section-title f3 purple" role="heading" aria-level="3">
                            Password
                        </div>

                        <div class="mt2 f5 lh-copy dark-gray">
                            Change the password here.
                        </div>
                    </div>

                    <div class="panel-content">
                        <div class="ember-view">
                            <div class="edit-first edit-password">
                                <form role="form" method="POST">
                                    <div class="form-group current-password-field">
                                        <label for="current-password">Current Password</label>
                                        <input name="password" @input="currentPasswordChange($event)"
                                               placeholder="enter your current password"
                                               id="current-password"
                                               class="mr2 mb2 w-100 mw6 form-control ember-text-field ember-view"
                                               type="password">
                                    </div>

                                    <div class="form-group">
                                        <label for="new-password">New
                                            Password</label>
                                        <input placeholder="enter a new password" @input="newPasswordChange($event)"
                                               id="new-password"
                                               class="mr2 mb2 w-100 mw6 form-control ember-text-field ember-view"
                                               type="password">
                                        <p class="f5 dark-gray pt2">
                                            Password must be 8 or more characters.
                                        </p>
                                    </div>

                                    <div class="form-group">
                                        <label for="confirm-new-password">Confirm
                                            New Password</label>
                                        <input placeholder="enter the password again"  @input="confirmNewPasswordChange($event)"
                                               id="confirm-new-password"
                                               class="mr2 mb2 w-100 mw6 form-control ember-text-field ember-view"
                                               type="password">
                                    </div>

                                    <div class="form-group">
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
            </li>
        </ul>
      </div>
  </div>
</div>
</template>

<script>
import AccountSetting from  "./AccountSetting"
export default AccountSetting
</script>
