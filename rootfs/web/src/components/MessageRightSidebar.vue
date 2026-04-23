<script setup lang="ts">
import { Settings, CheckCircle2, LifeBuoy, BookOpen, Activity, ArrowUpRight, ArrowRight } from 'lucide-vue-next'
import { globalState, fetchGlobalSettings, invalidateMessages } from '../store'
import { onMounted } from 'vue'
import { markAllAsRead } from '../services/messages'

const emit = defineEmits(['mark-all-read'])

onMounted(async () => {
    await fetchGlobalSettings()
})

const handleMarkAllAsRead = async () => {
    try {
        await markAllAsRead()
        invalidateMessages()
        emit('mark-all-read')
    } catch (e) {
        console.error('Failed to mark all as read', e)
    }
}
</script>

<template>
  <aside class="w-full lg:w-72 flex-shrink-0 space-y-5">
    
    <!-- Settings & Actions Card -->
    <div class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden relative overflow-y-hidden group">
      <!-- Decorative hover flare -->
      <div class="absolute -right-20 -top-20 w-40 h-40 bg-primary/5 rounded-full blur-2xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"></div>

      <div class="px-5 py-4 border-b border-slate-100 bg-slate-50/50 flex flex-col gap-1 relative z-10">
        <h3 class="text-[13px] font-semibold text-slate-800 flex items-center gap-2 uppercase tracking-wide">
          <Settings class="w-3.5 h-3.5 text-primary" />
          Actions
        </h3>
      </div>
      <div class="p-3 relative z-10">
        <button @click="handleMarkAllAsRead" class="w-full flex items-center justify-between px-3 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-50 hover:text-slate-900 rounded-lg transition-all group/item focus:outline-none">
          <span class="flex items-center gap-2.5">
            <CheckCircle2 class="w-4 h-4 text-emerald-400 group-hover/item:text-emerald-500 transition-colors" />
            Mark all as read
          </span>
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 opacity-0 group-hover/item:opacity-100 shadow-[0_0_4px_rgba(16,185,129,0.5)] transition-all"></span>
        </button>
        <router-link to="/messages/preferences" class="w-full flex items-center justify-between px-3 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-50 hover:text-slate-900 rounded-lg transition-all group/item mt-1 focus:outline-none">
          <span class="flex items-center gap-2.5">
            <Settings class="w-4 h-4 text-primary/60 group-hover/item:text-primary transition-colors" />
            Notification Preferences
          </span>
          <ArrowRight class="w-3.5 h-3.5 text-slate-300 group-hover/item:text-primary -translate-x-1 group-hover/item:translate-x-0 opacity-0 group-hover/item:opacity-100 transition-all" />
        </router-link>
      </div>
    </div>

    <!-- System Status Card -->
    <div class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden opacity-95 hover:opacity-100 transition-opacity">
      <div class="px-5 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center justify-between">
        <h3 class="text-[13px] font-semibold text-slate-800 flex items-center gap-2 uppercase tracking-wide">
          <BookOpen class="w-3.5 h-3.5 text-blue-500" />
          Pro Tips
        </h3>
      </div>
      <div class="p-5">
        <div class="space-y-4">
          <div class="flex gap-3 items-start group/tip cursor-default">
            <div class="w-6 h-6 rounded-md bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0 mt-0.5 group-hover/tip:bg-blue-100 transition-colors">
              <span class="text-[11px] font-bold">1</span>
            </div>
            <div>
              <h4 class="text-[13px] font-semibold text-slate-700 mb-0.5">Filter by Severity</h4>
              <p class="text-xs text-slate-500 leading-relaxed">Use the left sidebar to quickly isolate critical alerts or system updates.</p>
            </div>
          </div>
          
          <div class="flex gap-3 items-start group/tip cursor-default">
            <div class="w-6 h-6 rounded-md bg-indigo-50 text-indigo-600 flex items-center justify-center flex-shrink-0 mt-0.5 group-hover/tip:bg-indigo-100 transition-colors">
              <span class="text-[11px] font-bold">2</span>
            </div>
            <div>
              <h4 class="text-[13px] font-semibold text-slate-700 mb-0.5">Automate Workflows</h4>
              <p class="text-xs text-slate-500 leading-relaxed">Configure Webhooks in preferences to forward messages directly to Slack or Teams.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Support / Resources Card -->
    <div class="bg-gradient-to-b from-slate-800 to-slate-900 rounded-lg shadow-[0_4px_20px_-4px_rgba(15,23,42,0.3)] border border-slate-700 overflow-hidden text-white relative group">
      <!-- Decorative animated background dots -->
      <div class="absolute -right-6 top-8 w-24 h-24 bg-primary/30 rounded-full blur-3xl group-hover:bg-primary/40 transition-colors pointer-events-none"></div>
      <div class="absolute -left-10 -bottom-10 w-20 h-20 bg-blue-500/20 rounded-full blur-2xl group-hover:bg-blue-500/30 transition-colors pointer-events-none"></div>
      
      <div class="p-6 relative z-10">
        <h3 class="text-sm font-semibold mb-2.5 flex items-center gap-2">
          <div class="p-1.5 bg-white/10 rounded-md">
            <LifeBuoy class="w-4 h-4 text-blue-300" />
          </div>
          Need Assistance?
        </h3>
        <p class="text-[13px] text-slate-300 leading-relaxed mb-5 font-medium opacity-90">
          Our support team is here to help you 24/7 with enterprise-grade SLA and troubleshooting.
        </p>
        <div class="space-y-2.5">
          <a :href="globalState.contactSupportUrl" class="flex items-center justify-center gap-2 w-full py-2 px-4 bg-white hover:bg-slate-50 text-slate-900 text-[13px] font-semibold rounded-lg transition-all focus:outline-none shadow-sm hover:shadow active:scale-[0.98]">
            <LifeBuoy class="w-4 h-4 shrink-0" />
            Contact Support
          </a>
          <a href="https://www.drycc.cc/zh-cn/docs/" target="_blank" class="flex items-center justify-center gap-2 w-full py-2 px-4 bg-white/5 hover:bg-white/10 border border-white/10 text-[13px] font-semibold text-slate-200 hover:text-white rounded-lg transition-colors focus:outline-none">
            <BookOpen class="w-4 h-4 shrink-0 opacity-70" />
            Read Documentation
          </a>
        </div>
      </div>
    </div>

  </aside>
</template>