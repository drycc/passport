import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import {onBeforeMount, reactive, toRefs} from 'vue'
import MainNav from "../components/MainNav.vue";
import MainFooter from "../components/MainFooter.vue";
import { useRouter } from 'vue-router'
import { putAccount, putAccountPassword } from "../services/user";
import { Toast } from "vant"

export default {
    name: "AccountSetting",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-nav': MainNav,
        'main-footer': MainFooter,
    },
    setup() {
        const showBTN = "flex items-center mb2"
        const hiddenBTN = "flex items-center mb2 clip"
        const hiddenUpdateBTN = "async-button default hk-button--disabled-primary ember-view"
        const showUpdateBTN = "async-button default hk-button--primary ember-view"

        var currentPassword, newPassword, confirmNewPassword

        const router = useRouter()
        const state = reactive({
            user: Object,
            originUser: Object,
            emailBTN: hiddenBTN,
            nameBTN: hiddenBTN,
            firstNameBTN: hiddenBTN,
            lastNameBTN: hiddenBTN,
            updateBTN: hiddenUpdateBTN
        })

        onBeforeMount(async () => {
            state.user = JSON.parse(sessionStorage.getItem('user'))
            state.originUser = JSON.parse(sessionStorage.getItem('user'))
        })

        const updateUser = () => {
            sessionStorage.setItem('user', JSON.stringify(state.user))
            state.originUser = state.user
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
                Toast.fail("this email is not valid.")
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
                Toast.fail("Current Password and New Password are the same.")
            } else if( newPassword.length >= 8){
                Toast.fail("this New Password is not valid.")
            } else if (newPassword != confirmNewPassword){
                Toast.fail("New Password Confirm and New Password are different.")
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
            submitPassowrd
        }
    },
}
