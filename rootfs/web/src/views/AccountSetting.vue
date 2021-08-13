<!--app列表页-->
<template>
    <nav-bar />
    <div class="limit-width top-nav flex flex-column justify-center">
        <div class="main-content">
            <main-nav :is-account-setting-active="true"/>
        <ul>
            <li id="profile">
                <div class="panel-section ">
                    <div class="section-description">
                        <div class="section-title f3 purple" role="heading" aria-level="3">
                            Profile
                        </div>
                        <div class="mt2 f5 lh-copy dark-gray">
                            Your name or email address is your identity on Drycc and is used to log in.
                        </div>
                    </div>

                    <div class="panel-content">
                        <div class="avatar">
                        </div>
                        <div class="edit-first">
                            <div id="ember26" class="ember-view">
                                <div id="ember27" class="ember-view">
                                    <form role="form">
                                        <label class="hk-label db mb2"
                                               for="new-e-mail">Email
                                            Address</label>
                                        <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                            <input autocomplete="off" placeholder="Your email address" @input="emailInputChage($event)"  id="new-e-mail" :value=user.email
                                                   class="mr2 mb2 w-100 mw6 ember-text-field hk-input ember-view"
                                                   type="text">

                                            <div :class=emailBTN data-test-target="hk-inline-buttons">
                                                <button id="ember28" class="mr1 async-button default hk-button--primary ember-view" @click="submitEmail()"
                                                        type="button"> Save
                                                </button>
                                                <button id="ember29" class="async-button default hk-button--secondary ember-view" @click="cancelEmail()"
                                                        type="button"> Cancel
                                                </button>
                                            </div>
                                        </div>
                                        <div style="display: none" class="email_error">提示信息</div>
                                    </form>
                                </div>
                                <span id="ember30" class="confirmable-action ember-view"> </span>
                            </div>
                            <div id="ember32" class="ember-view">
                                <div id="ember33" class="ember-view">
                                    <form role="form">
                                        <label class="hk-label db mb2" for="name">Name
                                        </label>
                                        <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                            <input autocomplete="off" placeholder="Your name" @input="nameInputChage($event)" id="name" :value=user.username
                                                   class="mr2 mb2 w-100 mw6 ember-text-field hk-input ember-view"
                                                   type="text">
                                            <div :class=nameBTN data-test-target="hk-inline-buttons">
                                                <button id="ember34"
                                                        class="mr1 async-button default hk-button--primary ember-view" @click="submitName()"
                                                        type="button"> Save
                                                </button>
                                                <button id="ember35"
                                                        class="async-button default hk-button--secondary ember-view" @click="cancelName()"
                                                        type="button"> Cancel
                                                </button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </li>
            <li id="password" style="padding-top: 40px;margin-top: 40px; border-top: 1px solid #e7ebf3;">
                <div class="panel-section ">
                    <div class="section-description">
                        <div class="section-title f3 purple" role="heading" aria-level="3">
                            Password
                        </div>

                        <div class="mt2 f5 lh-copy dark-gray">
                            Changing your password will also reset your API key.
                        </div>
                    </div>

                    <div class="panel-content">
                        <div id="ember36" class="ember-view">
                            <div class="edit-first edit-password">
                                <form role="form" method="POST">
                                    <div class="form-group current-password-field">
                                        <label for="current-password">Current Password</label>
                                        <input name="password" @input="currentPasswordChage($event)"
                                               placeholder="enter your current password"
                                               id="current-password"
                                               class="form-control ember-text-field ember-view"
                                               type="password">
                                    </div>

                                    <div class="form-group">
                                        <label for="new-password">New
                                            Password</label>
                                        <input placeholder="enter a new password" @input="newPasswordChage($event)"
                                               id="new-password"
                                               class="form-control ember-text-field ember-view"
                                               type="password">
                                        <p class="f5 dark-gray pt2">
                                            Password must be 8 or more characters.
                                        </p>
                                    </div>

                                    <div class="form-group">
                                        <label for="confirm-new-password">Confirm
                                            New Password</label>
                                        <input placeholder="enter the password again"  @input="confirmNewPasswordChage($event)"
                                               id="confirm-new-password"
                                               class="form-control ember-text-field ember-view"
                                               type="password">
                                    </div>

                                    <div class="form-group">
                                        <button id="ember37" @click="submitPassowrd()"
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
</template>

<script>
import AccountSetting from  "./AccountSetting"
export default AccountSetting
</script>

<style scoped>
    /*@import "../assets/bashboard.css";*/
    .pr1 {
        padding-right: 15px;
    }
</style>
