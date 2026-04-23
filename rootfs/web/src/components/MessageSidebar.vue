<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Bell, ShieldAlert, Cpu, Activity, Info, AlertTriangle, Inbox, ArrowLeft } from 'lucide-vue-next'
import { globalState, fetchGlobalSettings } from '../store'

const route = useRoute()
const router = useRouter()

onMounted(async () => {
    await fetchGlobalSettings()
})

const isActive = (categoryId: string) => {
    if (route.path !== '/messages') return false
    const queryCat = route.query.category || 'all'
    return queryCat === categoryId
}

const navigateToCategory = (categoryId: string) => {
    if (categoryId === 'all') {
        router.push({ path: '/messages' })
    } else {
        router.push({ path: '/messages', query: { category: categoryId } })
    }
}
</script>

<template>
  <aside class="w-full lg:w-64 flex-shrink-0 flex flex-col gap-5">
      
      <!-- Back to Dashboard / Apps (since it replaces AppSidebar) -->
      <div>
          <a :href="globalState.dashboardUrl" class="w-full bg-white border border-slate-200 rounded-md px-3 py-2 flex items-center justify-center shadow-sm hover:border-primary transition-colors focus:outline-none group">
              <span class="flex items-center gap-2 text-sm text-slate-600 group-hover:text-primary transition-colors font-medium">
                  <ArrowLeft class="w-4 h-4" /> Back to Dashboard
              </span>
          </a>
      </div>

      <div class="flex flex-col gap-0.5 mt-2">
          <p class="text-xs font-semibold text-slate-500 mb-2 px-1">Message Types</p>
          
          <button @click="navigateToCategory('all')" :class="[
              'w-full flex items-center gap-3 px-3 py-2 rounded-md font-medium transition-all text-left focus:outline-none',
              isActive('all') 
                  ? 'bg-primary-50 text-primary' 
                  : 'text-slate-600 hover:bg-white hover:shadow-sm'
          ]">
              <Inbox :class="['w-4 h-4', isActive('all') ? 'text-primary' : 'text-slate-400']" /> All Messages
          </button>
          
          <div class="h-px bg-slate-200/80 my-2"></div>

          <button @click="navigateToCategory('system')" :class="[
              'w-full flex items-center gap-3 px-3 py-2 rounded-md font-medium transition-all text-left focus:outline-none',
              isActive('system') 
                  ? 'bg-primary-50 text-primary' 
                  : 'text-slate-600 hover:bg-white hover:shadow-sm'
          ]">
              <Info :class="['w-4 h-4', isActive('system') ? 'text-primary' : 'text-slate-400']" /> System
          </button>

          <button @click="navigateToCategory('product')" :class="[
              'w-full flex items-center gap-3 px-3 py-2 rounded-md font-medium transition-all text-left focus:outline-none',
              isActive('product') 
                  ? 'bg-primary-50 text-primary' 
                  : 'text-slate-600 hover:bg-white hover:shadow-sm'
          ]">
              <Cpu :class="['w-4 h-4', isActive('product') ? 'text-primary' : 'text-slate-400']" /> Product Updates
          </button>

          <button @click="navigateToCategory('security')" :class="[
              'w-full flex items-center gap-3 px-3 py-2 rounded-md font-medium transition-all text-left focus:outline-none',
              isActive('security') 
                  ? 'bg-primary-50 text-primary' 
                  : 'text-slate-600 hover:bg-white hover:shadow-sm'
          ]">
              <ShieldAlert :class="['w-4 h-4', isActive('security') ? 'text-primary' : 'text-slate-400']" /> Security
          </button>

          <button @click="navigateToCategory('alert')" :class="[
              'w-full flex items-center gap-3 px-3 py-2 rounded-md font-medium transition-all text-left focus:outline-none',
              isActive('alert') 
                  ? 'bg-primary-50 text-primary' 
                  : 'text-slate-600 hover:bg-white hover:shadow-sm'
          ]">
              <AlertTriangle :class="['w-4 h-4', isActive('alert') ? 'text-primary' : 'text-slate-400']" /> Alerts
          </button>

          <button @click="navigateToCategory('service')" :class="[
              'w-full flex items-center gap-3 px-3 py-2 rounded-md font-medium transition-all text-left focus:outline-none',
              isActive('service') 
                  ? 'bg-primary-50 text-primary' 
                  : 'text-slate-600 hover:bg-white hover:shadow-sm'
          ]">
              <Activity :class="['w-4 h-4', isActive('service') ? 'text-primary' : 'text-slate-400']" /> Service
          </button>

      </div>
  </aside>
</template>