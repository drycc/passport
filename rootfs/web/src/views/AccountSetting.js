import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import {onBeforeMount, reactive, toRefs} from 'vue'
import MainNav from "../components/MainNav.vue";
import { useRouter } from 'vue-router'
import { putAccount, putAccountPassword } from "../services/user";
import { Toast } from "vant"

export default {
    name: "AccountSetting",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-nav': MainNav,
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

        const emailInputChage = (event) => {
            let newEmail = event.currentTarget.value
            if (newEmail != state.originUser.email) {
                state.emailBTN = showBTN
            } else {
                state.emailBTN = hiddenBTN
            }
            state.user.email = newEmail
        }

        const nameInputChage = (event) => {
            let newName = event.currentTarget.value
            if (newName != state.originUser.username) {
                state.nameBTN = showBTN
            } else {
                state.nameBTN = hiddenBTN
            }
            state.user.username = newName
        }

        const currentPasswordChage = (event) => {
            currentPassword = event.currentTarget.value
            if (currentPassword && newPassword && confirmNewPassword) {
                state.updateBTN = showUpdateBTN
            } else {
                state.updateBTN = hiddenUpdateBTN
            }
        }
        const newPasswordChage = (event) => {
            newPassword = event.currentTarget.value
            if (currentPassword && newPassword && confirmNewPassword) {
                state.updateBTN = showUpdateBTN
            } else {
                state.updateBTN = hiddenUpdateBTN
            }
        }
        const confirmNewPasswordChage = (event) => {
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

        const submitName = () => {
            putAccount({username: state.user.username}).then(res=>{
                if (res.status == 204) {
                    updateUser()
                    state.nameBTN = hiddenBTN
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

        const cancelName = () => {
            state.nameBTN = hiddenBTN
            state.user.username = state.originUser.username
        }
        return {
            ...toRefs(state),
            emailInputChage,
            nameInputChage,
            submitEmail,
            cancelEmail,
            submitName,
            cancelName,
            currentPasswordChage,
            newPasswordChage,
            confirmNewPasswordChage,
            submitPassowrd
        }
    },
}
