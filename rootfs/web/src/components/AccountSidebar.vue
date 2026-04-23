<template>
    <aside class="w-full lg:w-64 flex-shrink-0 flex flex-col gap-5">
        <!-- Back to Dashboard -->
        <div>
            <a :href="globalState.dashboardUrl" class="w-full bg-white border border-slate-200 rounded-md px-3 py-2 flex items-center justify-center shadow-sm hover:border-primary transition-colors focus:outline-none group">
                <span class="flex items-center gap-2 text-sm text-slate-600 group-hover:text-primary transition-colors font-medium">
                    <ArrowLeft class="w-4 h-4" /> Back to Dashboard
                </span>
            </a>
        </div>

        <div class="flex flex-col gap-0.5 mt-2">
            <p class="text-xs font-semibold text-slate-500 mb-2 px-1">Settings</p>
            <button @click="goToAccessToken" 
                    class="flex items-center justify-start gap-3 px-3 py-2 transition-all w-full text-left"
                    :class="isAccessTokenActive ? 'bg-primary-50 text-primary rounded-md font-medium' : 'text-slate-600 hover:bg-white hover:shadow-sm rounded-md'"
                    type="button">
                <Key :class="isAccessTokenActive ? 'w-4 h-4' : 'w-4 h-4 text-slate-400'" />
                <span>Access Tokens</span>
            </button>
            <button @click="goToAccountSetting" 
                    class="flex items-center justify-start gap-3 px-3 py-2 transition-all w-full text-left"
                    :class="isAccountSettingActive ? 'bg-primary-50 text-primary rounded-md font-medium' : 'text-slate-600 hover:bg-white hover:shadow-sm rounded-md'"
                    type="button">
                <Settings :class="isAccountSettingActive ? 'w-4 h-4' : 'w-4 h-4 text-slate-400'" />
                <span>Account Setting</span>
            </button>
        </div>
    </aside>
</template>

<script lang="ts">
import { useRouter } from 'vue-router'
import { Key, Settings, ArrowLeft } from 'lucide-vue-next'
import { globalState, fetchGlobalSettings } from '../store'
import { onMounted } from 'vue'

export default {
    name: "AccountSidebar",
    components: {
        Key,
        Settings,
        ArrowLeft
    },
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
        
        onMounted(async () => {
            await fetchGlobalSettings()
        })

        const goToAccessToken = () => {
            router.push({ path: `/access-tokens` })
        }

        const goToAccountSetting = () => {
            router.push({ path: `/account-setting` })
        }

        return {
            globalState,
            goToAccessToken,
            goToAccountSetting,
        }
    },

}

</script>

<style scoped>
/* Scoped styles removed */
</style>
