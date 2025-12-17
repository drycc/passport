import { computed, markRaw, onBeforeMount, reactive, toRefs, watch } from "vue";
import { useRouter } from 'vue-router'
import {dealUser, getUser, postLogout} from "../services/user";
import { Key, Setting, SwitchButton, UserFilled } from "@element-plus/icons-vue";

export default {
    name: "UserMenu",
    props: {
        user: {
            type: Object,
            default: null
        }
    },
    setup(props) {
        const router = useRouter()
        const normalizeUser = (input) => {
            if (!input) {
                return {
                    username: null,
                    email: null,
                    first_name: null,
                    last_name: null
                }
            }
            if (input.data) {
                return dealUser(input)
            }
            return {
                username: input.username ?? null,
                email: input.email ?? null,
                first_name: input.first_name ?? null,
                last_name: input.last_name ?? null
            }
        }
        const state = reactive({
            user :{
                username: null,
                email: null,
                is_superuser: null
            },
        })
        const logout = () => {
            postLogout().then(res=>{
                if (res.status == 200) {
                    sessionStorage.clear()
                    router.push({ path: '/'})
                }
            })
            location.reload(true)
        }

        const accountTriggerIcon = markRaw(UserFilled)

        const menuItems = computed(() => [
            {
                key: "settings",
                label: "Settings",
                href: "/account-setting",
                icon: markRaw(Setting)
            },
            {
                key: "access-tokens",
                label: "Access Tokens",
                href: "/access-tokens",
                icon: markRaw(Key)
            },
            {
                key: "sign-out",
                label: "Sign Out",
                actionKey: "logout",
                icon: markRaw(SwitchButton)
            }
        ])

        const handleMenuAction = (actionKey) => {
            if (actionKey === "logout") {
                logout()
            }
        }

        watch(
            () => props.user,
            (newUser) => {
                if (newUser) {
                    state.user = normalizeUser(newUser)
                }
            },
            { immediate: true }
        )

        onBeforeMount(async () => {
            if (!props.user) {
                const res = await getUser()
                state.user = normalizeUser(res)
            }
        })

        return {
            ...toRefs(state),
            accountTriggerIcon,
            menuItems,
            handleMenuAction
        }
    }
}
