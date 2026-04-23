<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import MessageSidebar from '../components/MessageSidebar.vue'
import { ArrowLeft, BellRing, Mail, ShieldCheck, Check, Webhook, Link, Info, Cpu, AlertTriangle, Activity } from 'lucide-vue-next'
import MessageRightSidebar from '../components/MessageRightSidebar.vue'
import { getMessagePreferences, updateMessagePreferences } from '../services/messages'

const router = useRouter()

const settings = ref({
    emailAlerts: true,
    pushAlerts: false,
    webhookUrl: '',

    notifySecurity: true,
    notifySystem: true,
    notifyProduct: true,
    notifyAlerts: true,
    notifyService: true,
})

const isSaving = ref(false)
const saved = ref(false)
const loading = ref(false)

const fetchPreferences = async () => {
    loading.value = true
    try {
        const res = await getMessagePreferences()
        const data = res.data
        settings.value = {
            emailAlerts: data.email_alerts,
            pushAlerts: data.push_alerts,
            webhookUrl: data.webhook_url || '',
            notifySecurity: data.notify_security,
            notifySystem: data.notify_system,
            notifyProduct: data.notify_product,
            notifyAlerts: data.notify_alert,
            notifyService: data.notify_service,
        }
    } catch (e) {
        console.error('Failed to fetch preferences', e)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchPreferences()
})

const savePreferences = async () => {
    isSaving.value = true
    saved.value = false
    try {
        await updateMessagePreferences({
            email_alerts: settings.value.emailAlerts,
            push_alerts: settings.value.pushAlerts,
            webhook_url: settings.value.webhookUrl,
            notify_security: settings.value.notifySecurity,
            notify_system: settings.value.notifySystem,
            notify_product: settings.value.notifyProduct,
            notify_alert: settings.value.notifyAlerts,
            notify_service: settings.value.notifyService,
        })
        saved.value = true
        setTimeout(() => saved.value = false, 3000)
    } catch (e) {
        console.error('Failed to save preferences', e)
        alert('Failed to save preferences')
    } finally {
        isSaving.value = false
    }
}
</script>

<template>
<div class="min-h-screen bg-slate-50 flex flex-col font-sans">
    <NavBar />
    <main class="max-w-[1600px] w-full mx-auto p-6 flex flex-col lg:flex-row gap-6 flex-1">
        <MessageSidebar />
  <!-- 主内容区 -->
  <section class="flex-1 flex flex-col w-full min-w-0">
      <div class="bg-white rounded-lg shadow-sm border border-slate-200 min-h-[600px] flex flex-col flex-1 overflow-hidden">
          
          <!-- 导航栏 -->
          <div class="px-6 py-4 flex items-center justify-between border-b border-slate-100 bg-slate-50/40">
              <button @click="router.push('/messages')" class="inline-flex items-center text-sm font-medium text-slate-500 hover:text-slate-800 transition-colors focus:outline-none">
                  <ArrowLeft class="w-4 h-4 mr-2 text-slate-400" />
                  Back to Inbox
              </button>
          </div>

          <!-- 头部区域 -->
          <div class="px-8 md:px-12 pt-10 pb-8">
              <div class="flex items-start gap-4 md:gap-5 mb-2">
                  <div class="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 bg-primary/10 ring-4 ring-primary/5 mt-0.5">
                      <BellRing class="w-6 h-6 text-primary" />
                  </div>
                  <div>
                      <h1 class="text-xl md:text-[22px] font-bold text-slate-900 tracking-tight leading-tight mb-2">
                          Notification Preferences
                      </h1>
                      <p class="text-sm text-slate-500 leading-relaxed max-w-2xl">
                          Control how and when you want to be notified about activity in your workspace.
                      </p>
                  </div>
              </div>
          </div>

          <!-- 设置项内容区 -->
          <div class="px-8 md:px-12 pb-12 flex-1">
              
              <!-- 渠道设置 -->
              <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wider mb-4 border-b border-slate-100 pb-2">Delivery Channels</h3>
              
              <div class="space-y-6 mb-10">
                  <!-- 邮件通知 -->
                  <div class="flex items-center justify-between">
                      <div class="flex items-center gap-3">
                          <div class="w-10 h-10 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-500">
                              <Mail class="w-5 h-5" />
                          </div>
                          <div>
                              <p class="text-[15px] font-semibold text-slate-800">Email Notifications</p>
                              <p class="text-xs text-slate-500 mt-0.5">Receive alerts via your primary account email.</p>
                          </div>
                      </div>
                      <label class="relative inline-flex items-center cursor-pointer">
                          <input type="checkbox" class="sr-only peer" v-model="settings.emailAlerts" />
                          <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                      </label>
                  </div>

                  <!-- Webhook 推送通知 -->
                  <div class="flex flex-col">
                      <div class="flex items-center justify-between">
                          <div class="flex items-center gap-3">
                              <div class="w-10 h-10 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-500">
                                  <Webhook class="w-5 h-5" />
                              </div>
                              <div>
                                  <p class="text-[15px] font-semibold text-slate-800">Webhook / Push Notifications</p>
                                  <p class="text-xs text-slate-500 mt-0.5">Forward real-time alerts to an external HTTP entrypoint.</p>
                              </div>
                          </div>
                          <label class="relative inline-flex items-center cursor-pointer">
                              <input type="checkbox" class="sr-only peer" v-model="settings.pushAlerts" />
                              <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                          </label>
                      </div>
                      
                      <!-- Webhook URL Configure -->
                      <transition
                          enter-active-class="transition-all duration-300 ease-[cubic-bezier(0.4,0,0.2,1)]"
                          enter-from-class="opacity-0 max-h-0 -translate-y-2 pointer-events-none"
                          enter-to-class="opacity-100 max-h-[140px] translate-y-0 pointer-events-auto"
                          leave-active-class="transition-all duration-200 ease-[cubic-bezier(0.4,0,0.2,1)]"
                          leave-from-class="opacity-100 max-h-[140px] translate-y-0 pointer-events-auto"
                          leave-to-class="opacity-0 max-h-0 -translate-y-2 pointer-events-none"
                      >
                          <div v-show="settings.pushAlerts" class="mt-4 pl-[52px]">
                              <div class="flex flex-col gap-1.5">
                                  <label class="text-[13px] font-semibold text-slate-700">Payload URL</label>
                                  <div class="relative group/input">
                                      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                          <Link class="h-4 w-4 text-slate-400 group-focus-within/input:text-primary transition-colors" />
                                      </div>
                                      <input 
                                          type="url" 
                                          v-model="settings.webhookUrl"
                                          placeholder="https://yourapp.example.com/webhook"
                                          class="block w-full max-w-lg pl-[36px] pr-3 py-2 border border-slate-200 rounded-lg text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-[3px] focus:ring-primary/10 focus:border-primary transition-all bg-white shadow-sm"
                                      />
                                  </div>
                                  <p class="text-[12px] text-slate-500 mt-0.5">
                                      We will send a POST request with a JSON payload to this endpoint.
                                  </p>
                              </div>
                          </div>
                      </transition>
                  </div>
              </div>

              <!-- 消息类别设置 -->
              <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wider mb-4 border-b border-slate-100 pb-2">Notification Types</h3>
              
              <div class="space-y-6 mb-8">
                  <!-- Security Alerts -->
                  <div class="flex items-center justify-between">
                      <div class="flex items-center gap-3">
                          <div class="w-10 h-10 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-500">
                              <ShieldCheck class="w-5 h-5" />
                          </div>
                          <div>
                              <p class="text-[15px] font-semibold text-slate-800">Security Alerts</p>
                              <p class="text-xs text-slate-500 mt-0.5">Login attempts, password resets, and critical account events.</p>
                          </div>
                      </div>
                      <label class="relative inline-flex items-center cursor-pointer">
                          <input type="checkbox" class="sr-only peer" v-model="settings.notifySecurity" />
                          <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                      </label>
                  </div>

                  <!-- System Messages -->
                  <div class="flex items-center justify-between">
                      <div class="flex items-center gap-3">
                          <div class="w-10 h-10 rounded-lg bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-500">
                              <Info class="w-5 h-5" />
                          </div>
                          <div>
                              <p class="text-[15px] font-semibold text-slate-800">System Messages</p>
                              <p class="text-xs text-slate-500 mt-0.5">Workspace updates, billing, and general system settings.</p>
                          </div>
                      </div>
                      <label class="relative inline-flex items-center cursor-pointer">
                          <input type="checkbox" class="sr-only peer" v-model="settings.notifySystem" />
                          <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                      </label>
                  </div>

                  <!-- Product Updates -->
                  <div class="flex items-center justify-between">
                      <div class="flex items-center gap-3">
                          <div class="w-10 h-10 rounded-lg bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600">
                              <Cpu class="w-5 h-5" />
                          </div>
                          <div>
                              <p class="text-[15px] font-semibold text-slate-800">Product Updates</p>
                              <p class="text-xs text-slate-500 mt-0.5">New features, changelogs, and major platform announcements.</p>
                          </div>
                      </div>
                      <label class="relative inline-flex items-center cursor-pointer">
                          <input type="checkbox" class="sr-only peer" v-model="settings.notifyProduct" />
                          <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                      </label>
                  </div>

                  <!-- Alerts -->
                  <div class="flex items-center justify-between">
                      <div class="flex items-center gap-3">
                          <div class="w-10 h-10 rounded-lg bg-amber-50 border border-amber-100 flex items-center justify-center text-amber-500">
                              <AlertTriangle class="w-5 h-5" />
                          </div>
                          <div>
                              <p class="text-[15px] font-semibold text-slate-800">Alerts & Warnings</p>
                              <p class="text-xs text-slate-500 mt-0.5">Usage thresholds, quota limits, and critical warnings.</p>
                          </div>
                      </div>
                      <label class="relative inline-flex items-center cursor-pointer">
                          <input type="checkbox" class="sr-only peer" v-model="settings.notifyAlerts" />
                          <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                      </label>
                  </div>

                  <!-- Service Status -->
                  <div class="flex items-center justify-between">
                      <div class="flex items-center gap-3">
                          <div class="w-10 h-10 rounded-lg bg-rose-50 border border-rose-100 flex items-center justify-center text-rose-500">
                              <Activity class="w-5 h-5" />
                          </div>
                          <div>
                              <p class="text-[15px] font-semibold text-slate-800">Service Status</p>
                              <p class="text-xs text-slate-500 mt-0.5">Application crashes, deployment failures, and infrastructure changes.</p>
                          </div>
                      </div>
                      <label class="relative inline-flex items-center cursor-pointer">
                          <input type="checkbox" class="sr-only peer" v-model="settings.notifyService" />
                          <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                      </label>
                  </div>
              </div>

              <!-- 保存与提交区 -->
              <div class="mt-12 pt-6 border-t border-slate-100 flex items-center gap-4">
                  <button 
                      @click="savePreferences" 
                      :disabled="isSaving"
                      class="inline-flex flex-shrink-0 items-center justify-center w-36 py-2.5 bg-primary hover:bg-primary-600 disabled:opacity-70 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-lg shadow-sm transition-all focus:outline-none"
                  >
                      <span v-if="isSaving" class="flex items-center gap-2">
                        <svg class="animate-spin -ml-1 mr-1 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Saving...
                      </span>
                      <span v-else>Save Changes</span>
                  </button>

                  <transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0 translate-y-1" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
                      <div v-if="saved" class="flex items-center gap-1.5 text-sm font-medium text-emerald-600 bg-emerald-50 px-3 py-1.5 rounded-md">
                          <Check class="w-4 h-4" />
                          Preferences saved!
                      </div>
                  </transition>
              </div>

          </div>
      </div>
  </section>

  <!-- 右侧侧边栏 (Sidebar) -->
  <MessageRightSidebar />
    </main>
</div>
</template>
