<!--app列表页-->
<template>
<div class="min-h-screen bg-slate-50 flex flex-col font-sans" :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar :user="user" />
    <main class="max-w-[1600px] w-full mx-auto p-6 flex flex-col lg:flex-row gap-6 flex-1">
        <main-nav :is-account-setting-active="true"  />
        <section class="flex-1 flex flex-col">
        <div class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden flex-1 flex flex-col min-h-[600px]">
            <!-- Header -->
            <div class="px-6 py-5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h2 class="text-lg font-medium text-slate-800">Account Settings</h2>
                    <p class="text-sm text-slate-500 mt-1">Manage your personal information, security settings, and linked accounts.</p>
                </div>
            </div>
            <div class="flex flex-col w-full divide-y divide-slate-100">
            <div>
                <div class="p-6 sm:p-8 flex flex-col md:flex-row gap-8">
                    <div class="md:w-1/3 flex-shrink-0">
                        <h3 class="text-base font-medium text-slate-800 mb-1">
                            Profile
                        </h3>
                        <p class="text-sm text-slate-500 leading-relaxed md:pr-4">
                            Manage your basic account details. Your username is your unique identity on the platform.
                        </p>
                    </div>

                    <div class="md:w-2/3 flex-grow max-w-2xl">
                        
                        <div class="">
                            <div class="space-y-5">
                                <div>
                                    <div>
                                        <label class="block text-[13px] font-medium text-slate-700 mb-1.5" for="name">Username
                                        </label>
                                        <div class="flex items-center gap-3">
                                            <input autocomplete="off" placeholder="Your name"  id="username" :value="user.username"
                                                    class="flex-1 px-3 py-2 text-[13px] text-slate-700 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
                                                    disabled
                                                    type="text">
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <div>
                                        <form role="form">
                                            <label class="block text-[13px] font-medium text-slate-700 mb-1.5"
                                                   for="new-e-mail">Email
                                                Address</label>
                                            <div class="flex items-center gap-3">
                                                <input autocomplete="off" placeholder="Your email address" @input="emailInputChange($event)"  id="new-e-mail" :value=user.email
                                                       class="flex-1 px-3 py-2 text-[13px] text-slate-700 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
                                                       type="text">

                                                
                                            </div>
                                            <div style="display: none" class="text-red-500 text-[13px] mt-1">提示信息</div>
                                        </form>
                                    </div>
                                    <span class="confirmable-action"> </span>
                                </div>
                                <div>
                                    <div>
                                        <form role="form">
                                            <label class="block text-[13px] font-medium text-slate-700 mb-1.5" for="first-name">First Name
                                            </label>
                                            <div class="flex items-center gap-3">
                                                <input autocomplete="off" placeholder="Your first name" @input="firstNameInputChange($event)" id="first-name" :value=user.first_name
                                                       class="flex-1 px-3 py-2 text-[13px] text-slate-700 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
                                                       type="text">
                                                
                                            </div>
                                        </form>
                                    </div>
                                </div>
                                <div>
                                    <div>
                                        <form role="form">
                                            <label class="block text-[13px] font-medium text-slate-700 mb-1.5" for="last-name">Last Name
                                            </label>
                                            <div class="flex items-center gap-3">
                                                <input autocomplete="off" placeholder="Your last name" @input="lastNameInputChange($event)" id="last-name" :value=user.last_name
                                                       class="flex-1 px-3 py-2 text-[13px] text-slate-700 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
                                                       type="text">
                                                
                                            </div>
                                        </form>
                                    </div>
                                </div>
                                <div class="flex items-center justify-between mt-6">
                                    <p class="text-[13px] text-slate-500">Manage your avatar using <a href="https://gravatar.com" target="_blank" rel="noopener noreferrer" class="text-primary hover:text-primary-600 hover:underline">Gravatar</a>.</p>
                                    <button class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-primary rounded-md hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm" :disabled="!isProfileChanged" @click="submitProfile()" type="button">
                                        Update Profile
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <div class="p-6 sm:p-8 flex flex-col md:flex-row gap-8">
                    <div class="md:w-1/3 flex-shrink-0">
                        <h3 class="text-base font-medium text-slate-800 mb-1">
                            Password
                        </h3>

                        <p class="text-sm text-slate-500 leading-relaxed md:pr-4">
                            Ensure your account is using a secure password to stay protected.
                        </p>
                    </div>

                    <div class="md:w-2/3 flex-grow max-w-2xl">
                        <div>
                            <div class="">
                            <div class="space-y-5 ui-form-grid--password">
                                <form role="form" method="POST" class="ui-password-form space-y-5">
                                    <div>
                                        <label class="block text-sm font-medium text-slate-700 mb-1.5" for="current-password">Current Password</label>
                                        <input name="password" @input="currentPasswordChange($event)"
                                               placeholder="enter your current password"
                                               id="current-password"
                                               class="w-full px-3 py-2 text-sm text-slate-700 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
                                               type="password">
                                    </div>

                                    <div>
                                        <label class="block text-sm font-medium text-slate-700 mb-1.5" for="new-password">New
                                            Password</label>
                                        <input placeholder="enter a new password" @input="newPasswordChange($event)"
                                               id="new-password"
                                               class="w-full px-3 py-2 text-sm text-slate-700 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
                                               type="password">
                                        <p class="text-[13px] text-slate-500 mt-1">
                                            Password must be 8 or more characters.
                                        </p>
                                    </div>

                                    <div>
                                        <label class="block text-sm font-medium text-slate-700 mb-1.5" for="confirm-new-password">Confirm
                                            New Password</label>
                                        <input placeholder="enter the password again"  @input="confirmNewPasswordChange($event)"
                                               id="confirm-new-password"
                                               class="w-full px-3 py-2 text-sm text-slate-700 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
                                               :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500/20': passwordMismatch }"
                                               type="password">
                                        <p v-if="passwordMismatch" class="text-[13px] text-red-500 mt-1">
                                            Passwords do not match.
                                        </p>
                                    </div>
                                    <div class="flex justify-end mt-6">
                                        <button class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-primary rounded-md hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm" :disabled="!isPasswordFormValid" @click="submitPassowrd()" type="button">
                                            Update Passwd
                                        </button>
                                    </div>
                                </form>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <div class="p-6 sm:p-8 flex flex-col md:flex-row gap-8">
                    <div class="md:w-1/3 flex-shrink-0">
                        <h3 class="text-base font-medium text-slate-800 mb-1">
                            Linked SSO
                        </h3>
                        <p class="text-sm text-slate-500 leading-relaxed md:pr-4">
                            Manage linked OAuth identities for faster single sign-on access.
                        </p>
                    </div>
                    <div class="md:w-2/3 flex-grow max-w-2xl">
                        <div class="ui-identities-table-wrap">
                            <div class="w-full border border-slate-200 rounded-md shadow-sm overflow-hidden bg-white">
                                <ul class="divide-y divide-slate-100">
                                    <li v-for="scope in identities" :key="scope.email" class="flex flex-col sm:flex-row sm:items-center justify-between p-4 sm:p-5 hover:bg-slate-50 transition-colors gap-4">
                                        <div class="flex items-center gap-4">
                                            <div class="w-10 h-10 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center flex-shrink-0">
                                                <template v-if="getProviderIcon(scope.provider)">
                                                    <span class="w-5 h-5 flex items-center justify-center [&>svg]:w-full [&>svg]:h-full" v-html="getProviderIcon(scope.provider)"></span>
                                                </template>
                                                <template v-else-if="scope.provider === 'github'">
                                                    <i data-lucide="github" class="w-5 h-5 text-slate-700"></i>
                                                </template>
                                                <template v-else-if="scope.provider === 'gitlab'">
                                                    <i data-lucide="gitlab" class="w-5 h-5 text-orange-600"></i>
                                                </template>
                                                <template v-else-if="scope.provider === 'gitee'">
                                                    <i data-lucide="git-merge" class="w-5 h-5 text-red-600"></i>
                                                </template>
                                                <template v-else>
                                                    <span class="font-bold text-slate-400">{{ scope.provider.charAt(0).toUpperCase() }}</span>
                                                </template>
                                            </div>
                                            <div class="flex flex-col">
                                                <span class="font-medium text-[14px] text-slate-800">
                                                    <template v-if="scope.provider === 'github'">GitHub</template>
                                                    <template v-else-if="scope.provider === 'gitlab'">GitLab</template>
                                                    <template v-else-if="scope.provider === 'gitee'">Gitee</template>
                                                    <template v-else>{{ scope.provider.charAt(0).toUpperCase() + scope.provider.slice(1) }}</template>
                                                </span>
                                                <span class="text-[13px] text-slate-500 mt-0.5">{{ scope.email }}</span>
                                            </div>
                                        </div>
                                        <button class="text-red-500 hover:text-red-700 hover:bg-red-50 px-3 py-1.5 rounded-md text-[13px] font-medium transition-colors border border-transparent hover:border-red-200 w-full sm:w-auto" @click="handleUnlink(scope)">
                                            Unlink Identity
                                        </button>
                                    </li>
                                    <li v-if="!identities || identities.length === 0">
                                        <div class="px-6 py-10 flex flex-col items-center justify-center text-center">
                                            <div class="w-12 h-12 bg-slate-50 border border-slate-100 rounded-full flex items-center justify-center mb-3">
                                                <i data-lucide="link-2" class="w-5 h-5 text-slate-400"></i>
                                            </div>
                                            <p class="text-[14px] font-medium text-slate-700">No linked SSO accounts</p>
                                            <p class="text-[13px] text-slate-500 mt-1">You haven't linked any third-party accounts yet.</p>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <div class="p-6 sm:p-8 flex flex-col md:flex-row gap-8">
                    <div class="md:w-1/3 flex-shrink-0">
                        <h3 class="text-base font-medium text-slate-800 mb-1">
                            Link New SSO
                        </h3>
                        <p class="text-sm text-slate-500 leading-relaxed md:pr-4">
                            Choose a provider to link a new OAuth identity.
                        </p>
                    </div>
                    <div class="md:w-2/3 flex-grow max-w-2xl">
                        <div v-if="providers.length === 0" class="ui-left-align">
                            
                        </div>
                        <div v-else class="ui-sso-providers-wrap">
                            <div class="flex flex-wrap gap-3 ui-sso-providers-list">
                                <button class="inline-flex items-center justify-center gap-2 bg-white border border-slate-200 hover:border-slate-300 hover:bg-slate-50 hover:text-slate-900 text-slate-700 rounded-md py-2 px-4 shadow-sm transition-all focus:outline-none focus:ring-2 focus:ring-slate-200 text-[13px] font-medium"
                                    v-for="provider in providers"
                                    :key="provider.name"
                                    @click.prevent="handleLink(provider)"
                                >
                                    <span class="w-4 h-4 flex items-center justify-center [&>svg]:w-full [&>svg]:h-full" v-html="provider.icon"></span>
                                    <span>Link {{ provider.name.charAt(0).toUpperCase() + provider.name.slice(1) }}</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            </div> <!-- Close flex flex-col w-full divide-y -->
        </div> <!-- Close bg-white rounded-lg -->
        </section>

        <!-- Right Sidebar (Profile & Help) -->
        <aside class="hidden xl:flex flex-col w-[280px] flex-shrink-0 gap-5">
            <!-- SSO & Security Guide -->
            <div class="bg-white rounded border border-slate-200 overflow-hidden">
                <div class="px-5 py-3.5 border-b border-slate-100 bg-white">
                    <h3 class="text-[13px] font-semibold text-slate-700">Security Guidance</h3>
                </div>
                <div class="p-5">
                    <p class="text-[12px] text-slate-500 leading-relaxed mb-4">
                        Link your third-party OAuth accounts to enable seamless one-click sign-in and ensure account recovery access.
                    </p>
                    <a href="https://oauth.net" target="_blank" class="text-[12px] font-medium text-primary hover:text-primary-600 flex items-center gap-1 transition-colors">
                        Learn more about SSO
                    </a>
                </div>
            </div>
            
            <!-- Extra Documentation Link -->
            <div class="bg-white rounded border border-slate-200 overflow-hidden">
                <div class="px-5 py-3.5 border-b border-slate-100 bg-white">
                    <h3 class="text-[13px] font-semibold text-slate-700">Need Help?</h3>
                </div>
                <div class="p-0">
                    <ul class="divide-y divide-slate-100">
                        <li>
                            <a href="https://www.drycc.cc" target="_blank" rel="noopener noreferrer" class="px-5 py-3 text-[12px] text-slate-600 hover:text-slate-900 hover:bg-slate-50 flex items-center justify-between transition-colors w-full">
                                <span>API Documentation</span>
                                <i data-lucide="external-link" class="w-3.5 h-3.5 text-slate-400"></i>
                            </a>
                        </li>
                        <li>
                            <a href="https://drycc.slack.com/" target="_blank" rel="noopener noreferrer" class="px-5 py-3 text-[12px] text-slate-600 hover:text-slate-900 hover:bg-slate-50 flex items-center justify-between transition-colors w-full">
                                <span>Community Support</span>
                                <i data-lucide="external-link" class="w-3.5 h-3.5 text-slate-400"></i>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </aside>
    </main>
    <main-footer />
</div>
</template>
<style scoped></style>
<script lang="ts">
import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import {onMounted, reactive, toRefs, computed} from 'vue'
import MainNav from "../components/MainNav.vue";
import MainFooter from "../components/MainFooter.vue";
import { useRouter } from 'vue-router'
import { dealUser, getUser, putAccount, putAccountPassword } from "../services/user";
const ElMessage = { success: alert, error: alert }
import { getIdentityProviders, getLinkedIdentities, unlinkIdentity } from "../services/identities";

export default {
    name: "AccountSetting",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-nav': MainNav,
        'main-footer': MainFooter,
    },
    setup() {
        const showBTN = "ui-inline-actions"
        const hiddenBTN = "ui-inline-actions is-hidden"

        const router = useRouter()
        const state = reactive({
            user: {
                username: null,
                email: null,
                first_name: null,
                last_name: null
            },
            originUser: {
                username: null,
                email: null,
                first_name: null,
                last_name: null
            },
            passwords: {
                current: '',
                new: '',
                confirm: ''
            },
            emailBTN: hiddenBTN,
            nameBTN: hiddenBTN,
            firstNameBTN: hiddenBTN,
            lastNameBTN: hiddenBTN,
            providers: [],
            identities: [],
            loading: false,
        })

        const isProfileChanged = computed(() => {
            return state.user.email !== state.originUser.email || 
                   state.user.first_name !== state.originUser.first_name || 
                   state.user.last_name !== state.originUser.last_name;
        })

        const isPasswordFormValid = computed(() => {
            return state.passwords.current && state.passwords.new && state.passwords.confirm;
        })

        const passwordMismatch = computed(() => {
            if (!state.passwords.new || !state.passwords.confirm) return false;
            return state.passwords.new !== state.passwords.confirm;
        })

        onMounted(async () => {
            const res = await getUser()
            const userData = dealUser(res)
            state.user = { ...userData }
            state.originUser = { ...userData }
            await fetchProviders()
            await fetchIdentities()
        })

        const fetchProviders = async () => {
            state.loading = true
            try {
                const res = await getIdentityProviders()
                state.providers = res.data?.results || []
            } finally {
                state.loading = false
            }
        }

        const fetchIdentities = async () => {
            state.loading = true
            try {
                const res = await getLinkedIdentities()
                state.identities = res.data?.results || []
            } finally {
                state.loading = false
            }
        }

        const handleLink = (provider) => {
            if (!provider?.login_url) {
                ElMessage.error("Provider login URL missing.")
                return
            }
            window.location.href = provider.login_url
        }

        const handleUnlink = async (identity) => {
            if (!identity?.id) {
                return
            }
            await unlinkIdentity(identity.id)
            ElMessage.success("Unlinked successfully.")
            await fetchIdentities()
        }

        const updateUser = () => {
            state.originUser = { ...state.user }
        }

        const emailInputChange = (event) => {
            let newEmail = event.currentTarget.value
            if (newEmail != state.originUser.email) {
                state.emailBTN = showBTN
            } else {
                state.emailBTN = hiddenBTN
            }
            state.user.email = newEmail
        }

        const firstNameInputChange = (event) => {
            let newFirstName = event.currentTarget.value
            if (newFirstName != state.originUser.first_name) {
                state.firstNameBTN = showBTN
            } else {
                state.firstNameBTN = hiddenBTN
            }
            state.user.first_name = newFirstName
        }

        const lastNameInputChange = (event) => {
            let newLastName = event.currentTarget.value
            if (newLastName != state.originUser.last_name) {
                state.lastNameBTN = showBTN
            } else {
                state.lastNameBTN = hiddenBTN
            }
            state.user.last_name = newLastName
        }

        const currentPasswordChange = (event) => {
            state.passwords.current = event.currentTarget.value
        }
        const newPasswordChange = (event) => {
            state.passwords.new = event.currentTarget.value
        }
        const confirmNewPasswordChange = (event) => {
            state.passwords.confirm = event.currentTarget.value
        }
        const submitProfile = () => {
            var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
            if(!re.test(state.user.email)) {
                ElMessage.error("This email is not valid.")
                return;
            }
            putAccount({
              email: state.user.email,
              first_name: state.user.first_name,
              last_name: state.user.last_name
            }).then(res=>{
                if (res.status == 204) {
                    updateUser()
                    ElMessage.success("Profile updated successfully")
                }
            })
        }

        const submitPassowrd = () => {
            if (state.passwords.current == state.passwords.new){
                ElMessage.error("Current Password and New Password are the same.")
            } else if( state.passwords.new.length < 8){
                ElMessage.error("this New Password is not valid.")
            } else if (state.passwords.new != state.passwords.confirm){
                ElMessage.error("New Password Confirm and New Password are different.")
            }else {
                putAccountPassword({password: state.passwords.current, new_password: state.passwords.new}).then(res=>{
                    if (res.status == 204) {
                        router.push({ path: `/` })
                    }
                })
            }
        }

        const cancelEmail = () => {
            state.emailBTN = hiddenBTN
            state.user.email = state.originUser.email
        }

        const cancelFirstName = () => {
            state.firstNameBTN = hiddenBTN
            state.user.first_name = state.originUser.first_name
        }

        const cancelLastName = () => {
            state.lastNameBTN = hiddenBTN
            state.user.last_name = state.originUser.last_name
        }

        const getProviderIcon = (providerName) => {
            const provider = state.providers.find((p) => p.name === providerName)
            if (provider) {
                return provider.icon
            }
            return null
        }

        return {
            getProviderIcon,
            ...toRefs(state),
            isProfileChanged,
            isPasswordFormValid,
            passwordMismatch,
            emailInputChange,
            firstNameInputChange,
            lastNameInputChange,
            submitProfile,
            currentPasswordChange,
            newPasswordChange,
            confirmNewPasswordChange,
            submitPassowrd,
            handleLink,
            handleUnlink
        }
    },
}

</script>
