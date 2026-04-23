<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import MainFooter from '../components/MainFooter.vue'
import { Settings, Key, Bell, ArrowLeft, ShieldCheck } from 'lucide-vue-next'
import { globalState, fetchGlobalSettings } from '../store'

const router = useRouter()

onMounted(async () => {
    await fetchGlobalSettings()
})
</script>

<template>
<div class="min-h-screen bg-slate-50 flex flex-col font-sans selection:bg-primary/10">
    <NavBar />
    
    <main class="max-w-[1200px] w-full mx-auto p-6 md:p-10 flex-1 flex flex-col transition-all duration-300">
        <!-- Hero Section -->
        <div class="flex flex-col items-center text-center mt-10 md:mt-16 mb-16 animate-fade-in-up">
            <div class="w-20 h-20 bg-gradient-to-tr from-primary to-primary-600 rounded-2xl shadow-lg shadow-primary/20 flex items-center justify-center mb-8 relative">
                <div class="absolute inset-0 bg-white/20 rounded-2xl blur-sm opacity-50"></div>
                <ShieldCheck class="w-10 h-10 text-white relative z-10" stroke-width="1.5" />
            </div>
            <h1 class="text-4xl md:text-5xl font-extrabold text-slate-800 tracking-tight mb-4">
                Identity & Security
            </h1>
            <p class="text-lg text-slate-500 max-w-2xl leading-relaxed">
                Manage your personal identity, security preferences, API access tokens, and stay updated with crucial system notifications.
            </p>
        </div>

        <!-- Modules Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 max-w-5xl mx-auto w-full mb-12">
            
            <!-- Cards -->
            <div @click="router.push('/account-setting')" class="group relative bg-white rounded-2xl shadow-sm border border-slate-200 p-8 hover:shadow-xl hover:-translate-y-1.5 hover:border-primary/30 transition-all duration-300 cursor-pointer overflow-hidden">
                <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-blue-50 to-transparent rounded-bl-full -mr-8 -mt-8 opacity-50 group-hover:opacity-100 transition-opacity"></div>
                <div class="w-14 h-14 bg-blue-50/80 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 relative z-10 text-blue-500 shadow-sm border border-blue-100/50">
                    <Settings class="w-7 h-7" stroke-width="1.5" />
                </div>
                <h2 class="text-xl font-bold text-slate-800 mb-3 relative z-10 group-hover:text-blue-600 transition-colors">Account Setting</h2>
                <p class="text-sm text-slate-500 leading-relaxed relative z-10">Update your basic profile, modify login credentials, and review linked identity providers.</p>
            </div>

            <div @click="router.push('/access-tokens')" class="group relative bg-white rounded-2xl shadow-sm border border-slate-200 p-8 hover:shadow-xl hover:-translate-y-1.5 hover:border-primary/30 transition-all duration-300 cursor-pointer overflow-hidden">
                <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-indigo-50 to-transparent rounded-bl-full -mr-8 -mt-8 opacity-50 group-hover:opacity-100 transition-opacity"></div>
                <div class="w-14 h-14 bg-indigo-50/80 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 relative z-10 text-indigo-500 shadow-sm border border-indigo-100/50">
                    <Key class="w-7 h-7" stroke-width="1.5" />
                </div>
                <h2 class="text-xl font-bold text-slate-800 mb-3 relative z-10 group-hover:text-indigo-600 transition-colors">Access Tokens</h2>
                <p class="text-sm text-slate-500 leading-relaxed relative z-10">Securely generate and manage API keys for your automated workflows and CLI authentications.</p>
            </div>

            <div @click="router.push('/messages')" class="group relative bg-white rounded-2xl shadow-sm border border-slate-200 p-8 hover:shadow-xl hover:-translate-y-1.5 hover:border-primary/30 transition-all duration-300 cursor-pointer overflow-hidden">
                <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-rose-50 to-transparent rounded-bl-full -mr-8 -mt-8 opacity-50 group-hover:opacity-100 transition-opacity"></div>
                <div class="w-14 h-14 bg-rose-50/80 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 relative z-10 text-rose-500 shadow-sm border border-rose-100/50">
                    <Bell class="w-7 h-7" stroke-width="1.5" />
                    <!-- Unread marker -->
                    <span class="absolute top-[14px] right-[14px] w-2.5 h-2.5 bg-rose-500 border-2 border-rose-50 rounded-full animate-pulse group-hover:bg-rose-400"></span>
                </div>
                <h2 class="text-xl font-bold text-slate-800 mb-3 relative z-10 group-hover:text-rose-600 transition-colors">Message Center</h2>
                <p class="text-sm text-slate-500 leading-relaxed relative z-10">Read important system alerts, review security notifications, and track platform updates.</p>
            </div>
        </div>

        <!-- Back to Dashboard Link -->
        <div class="mt-auto flex justify-center pb-8 w-full">
            <a :href="globalState.dashboardUrl" class="group flex items-center gap-2.5 text-slate-500 hover:text-primary font-semibold transition-all border border-slate-200 bg-white px-8 py-3.5 rounded-full hover:shadow-md hover:border-primary/30">
                <ArrowLeft class="w-[18px] h-[18px] group-hover:-translate-x-1.5 transition-transform" /> 
                Enter Workspace Dashboard
            </a>
        </div>

    </main>

    <MainFooter class="mt-auto" />
</div>
</template>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translate3d(0, 20px, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
}
</style>
