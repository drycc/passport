<!--用户菜单-->
<template>
    <dropdown
        v-if="currentUser && currentUser.username != null"
        trigger-id="menu-account"
        menu-id="ui-user-menu--account"
        trigger-label="Account"
        :trigger-icon="accountTriggerIcon"
        :items="menuItems"
        meta-label="Signed in as"
        :meta-value="currentUser?.email || currentUser?.username"
        :menu-width="226"
        :hide-label-on-mobile="true"
        @action="handleMenuAction"
    >
    </dropdown>
</template>

<script lang="ts">
import { computed, markRaw, onBeforeMount, reactive, toRefs, watch } from "vue";
import { useRouter } from 'vue-router'
import {dealUser, getUser, postLogout} from "../services/user";
import { Key, Settings, LogOut, User } from "lucide-vue-next";
import Dropdown from "./Dropdown.vue";

export default {
    name: "UserMenu",
    components: { Dropdown },
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
            currentUser :{
                username: null,
                email: null,
                first_name: null,
                last_name: null,
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
            location.reload()
        }

        const accountTriggerIcon = markRaw(User)

        const userInitials = computed(() => {
            if (state.currentUser?.first_name) {
                return state.currentUser.first_name.charAt(0).toUpperCase()
            }
            if (state.currentUser?.username) {
                return state.currentUser.username.charAt(0).toUpperCase()
            }
            if (state.currentUser?.email) {
                return state.currentUser.email.charAt(0).toUpperCase()
            }
            return 'A'
        })

        const menuItems = computed(() => [
            {
                key: "settings",
                label: "Settings",
                href: "/account-setting",
                icon: markRaw(Settings)
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
                icon: markRaw(LogOut)
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
                    state.currentUser = normalizeUser(newUser)
                }
            },
            { immediate: true }
        )

        onBeforeMount(async () => {
            if (!props.user) {
                const res = await getUser()
                state.currentUser = normalizeUser(res)
            }
        })

        return {
            ...toRefs(state),
            accountTriggerIcon,
            menuItems,
            userInitials,
            handleMenuAction
        }
    }
}

</script>
