<!--导航栏-->
<template>
  <header class="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm w-full">
    <div class="max-w-[1600px] w-full mx-auto flex items-center justify-between px-6 py-2.5 h-14">
      <!-- Logo -->
      <div class="flex items-center">
          <router-link to="/" class="flex items-center gap-2.5 hover:opacity-80 transition-opacity">
              <div class="flex items-center justify-center w-8 h-8 bg-primary rounded shadow-sm">
                  <img class="w-5 h-5 object-contain filter brightness-0 invert" src="../../src/assets/icons/drycc.svg" alt="Drycc" />
              </div>
              <span class="text-base font-semibold text-slate-800 tracking-tight">Drycc CaaS</span>
          </router-link>
      </div>
      
      <!-- 右侧导航与工具栏合并 -->
      <div class="flex items-center gap-3">
          <div class="hidden lg:flex items-center text-sm font-medium text-slate-600">
              <nav-menu />
          </div>
          
          <!-- 分隔线 -->
          <div class="w-px h-4 bg-slate-200 hidden lg:block mx-0.5"></div>

          <div class="flex items-center gap-1.5 text-slate-500">
              <!-- 通知/消息中心 (Inbox) -->
              <div class="relative group">
                  <button @click="$router.push('/messages')" class="relative flex items-center justify-center w-8 h-8 text-slate-500 hover:text-slate-700 bg-transparent hover:bg-slate-50 rounded-lg transition-colors focus:outline-none" type="button" aria-label="Notifications">
                      <Inbox class="w-[18px] h-[18px] stroke-[2]" aria-hidden="true" />
                      <!-- 新消息指示器：完美嵌入右上角边缘 -->
                      <span v-if="unreadCount > 0" class="absolute top-[4px] right-[4px] flex h-2 w-2">
                          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                          <span class="relative inline-flex rounded-full h-[7px] w-[7px] bg-rose-500 ring-[1.5px] ring-white"></span>
                      </span>
                  </button>

                  <!-- 下拉消息面板 (Hover 显示) -->
                  <div class="absolute top-full right-0 mt-2 w-80 bg-white border border-slate-200 shadow-[0_10px_40px_-10px_rgba(0,0,0,0.1)] rounded-xl z-50 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform origin-top translate-y-2 group-hover:translate-y-0 cursor-default">
                      <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between bg-slate-50/50 rounded-t-xl">
                          <h3 class="text-xs font-semibold text-slate-800 uppercase tracking-wider">Inbox</h3>
                          <button @click="handleMarkAllRead" class="text-[11px] text-primary hover:text-primary-700 font-medium transition-colors">Mark all read</button>
                      </div>
                      <div class="max-h-[320px] overflow-y-auto w-full">
                          <div v-if="loading" class="px-4 py-6 text-center text-xs text-slate-400">Loading...</div>
                          <div v-else-if="recentMessages.length === 0" class="px-4 py-6 text-center text-xs text-slate-400">No messages</div>
                          <router-link
                              v-for="msg in recentMessages"
                              :key="msg.id"
                              :to="`/messages/${msg.id}`"
                              class="block px-4 py-3 hover:bg-slate-50 border-b border-slate-50 last:border-0 transition-colors relative group/item"
                          >
                              <span v-if="!msg.isRead" class="absolute left-2.5 top-4 w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_4px_rgba(16,185,129,0.5)]"></span>
                              <div class="pl-3">
                                  <p class="text-xs font-semibold mb-1 group-hover/item:text-primary transition-colors" :class="msg.isRead ? 'text-slate-600' : 'text-slate-800'">{{ msg.title }}</p>
                                  <p class="text-[11px] text-slate-500 leading-snug line-clamp-2 mb-1.5">{{ msg.content }}</p>
                                  <p class="text-[10px] text-slate-400 font-medium">{{ formatTime(msg.date) }}</p>
                              </div>
                          </router-link>
                      </div>
                      <div class="px-4 py-2 border-t border-slate-100 text-center rounded-b-xl bg-slate-50/50">
                          <router-link to="/messages" class="text-[11px] text-slate-500 hover:text-slate-800 font-semibold transition-colors">View all activity</router-link>
                      </div>
                  </div>
              </div>

              <!-- Account -->
              <user-menu :user="user" />
          </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { Inbox } from "lucide-vue-next";
import NavMenu from "./NavMenu.vue";
import UserMenu from "./UserMenu.vue";
import { getMessages, dealMessages, markAllAsRead } from '../services/messages'
import { globalState, invalidateMessages } from '../store'

defineProps<{
    user?: object
}>()

const recentMessages = ref<any[]>([])
const loading = ref(false)

const unreadCount = computed(() => recentMessages.value.filter(m => !m.isRead).length)

const fetchRecentMessages = async () => {
    loading.value = true
    try {
        const res = await getMessages('all', 5, 0)
        const payload = dealMessages(res)
        recentMessages.value = payload.results
    } catch (e) {
        console.error('Failed to fetch recent messages', e)
    } finally {
        loading.value = false
    }
}

const handleMarkAllRead = async () => {
    try {
        await markAllAsRead()
        recentMessages.value.forEach(m => m.isRead = true)
        invalidateMessages()
    } catch (e) {
        console.error('Failed to mark all as read', e)
    }
}

onMounted(() => {
    fetchRecentMessages()
})

// Refresh when other components signal that message read-state changed.
watch(() => globalState.messagesVersion, () => {
    fetchRecentMessages()
})

const formatTime = (dateStr: string) => {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)
    if (minutes < 1) return 'Just now'
    if (minutes < 60) return `${minutes}m ago`
    if (hours < 24) return `${hours}h ago`
    if (days < 7) return `${days}d ago`
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}
</script>

<style scoped>
/* Scoped styles removed */
</style>
