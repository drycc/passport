import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import {onMounted, reactive, toRefs} from 'vue'
import MainNav from "../components/MainNav.vue";
import MainFooter from "../components/MainFooter.vue";
import { useRouter } from 'vue-router'
import { dealUser, getUser, putAccount, putAccountPassword } from "../services/user";
import { showFailToast, showSuccessToast } from "vant"
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
        const hiddenUpdateBTN = "ui-btn ui-btn--primary is-disabled"
        const showUpdateBTN = "ui-btn ui-btn--primary"

        var currentPassword, newPassword, confirmNewPassword

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
            emailBTN: hiddenBTN,
            nameBTN: hiddenBTN,
            firstNameBTN: hiddenBTN,
            lastNameBTN: hiddenBTN,
            updateBTN: hiddenUpdateBTN,
            providers: [],
            identities: [],
            loading: false,
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
                showFailToast("Provider login URL missing.")
                return
            }
            window.location.href = provider.login_url
        }

        const handleUnlink = async (identity) => {
            if (!identity?.id) {
                return
            }
            await unlinkIdentity(identity.id)
            showSuccessToast("Unlinked successfully.")
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
            currentPassword = event.currentTarget.value
            if (currentPassword && newPassword && confirmNewPassword) {
                state.updateBTN = showUpdateBTN
            } else {
                state.updateBTN = hiddenUpdateBTN
            }
        }
        const newPasswordChange = (event) => {
            newPassword = event.currentTarget.value
            if (currentPassword && newPassword && confirmNewPassword) {
                state.updateBTN = showUpdateBTN
            } else {
                state.updateBTN = hiddenUpdateBTN
            }
        }
        const confirmNewPasswordChange = (event) => {
            confirmNewPassword = event.currentTarget.value
            if (currentPassword && newPassword && confirmNewPassword) {
                state.updateBTN = showUpdateBTN
            } else {
                state.updateBTN = hiddenUpdateBTN
            }
        }
        const submitEmail = () => {
            var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
            if(!re.test(state.user.email)) {
                showFailToast("this email is not valid.")
            } else {
                putAccount({email: state.user.email}).then(res=>{
                    if (res.status == 204) {
                        updateUser()
                        state.emailBTN = hiddenBTN
                    }
                })
            }
        }

        const submitFirstName = () => {
            putAccount({first_name: state.user.first_name}).then(res=>{
                if (res.status == 204) {
                    updateUser()
                    state.firstNameBTN = hiddenBTN
                }
            })
        }

        const submitLastName = () => {
            putAccount({last_name: state.user.last_name}).then(res=>{
                if (res.status == 204) {
                    updateUser()
                    state.lastNameBTN = hiddenBTN
                }
            })
        }

        const submitPassowrd = () => {
            if (currentPassword == newPassword){
                showFailToast("Current Password and New Password are the same.")
            } else if( newPassword.length < 8){
                showFailToast("this New Password is not valid.")
            } else if (newPassword != confirmNewPassword){
                showFailToast("New Password Confirm and New Password are different.")
            }else {
                putAccountPassword({password: currentPassword, new_password: newPassword}).then(res=>{
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

        return {
            ...toRefs(state),
            emailInputChange,
            firstNameInputChange,
            lastNameInputChange,
            submitEmail,
            cancelEmail,
            submitFirstName,
            cancelFirstName,
            submitLastName,
            cancelLastName,
            currentPasswordChange,
            newPasswordChange,
            confirmNewPasswordChange,
            submitPassowrd,
            handleLink,
            handleUnlink
        }
    },
}
