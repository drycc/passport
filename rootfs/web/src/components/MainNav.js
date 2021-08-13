import { reactive, toRefs} from 'vue'
import { useRouter } from 'vue-router'

export default {
    name: "MainNav",
    props: {
        isAccessTokenActive: {
            type: Boolean,
            default: false
        },
        isAccountSettingActive: {
            type: Boolean,
            default: false
        },
    },
    setup(props) {
        const router = useRouter()
        const goToAccessToken = () => {
            router.push({ path: `/access-tokens` })
        }

        const goToAccountSetting = () => {
            router.push({ path: `/account-setting` })
        }

        return {
            goToAccessToken,
            goToAccountSetting,
        }
    },

}
