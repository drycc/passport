<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import NavBar from '../components/NavBar.vue'
import MessageSidebar from '../components/MessageSidebar.vue'
import { useRoute } from 'vue-router'
import { Bell, ShieldAlert, Cpu, Activity, Info, AlertTriangle, ChevronRight, Search } from 'lucide-vue-next'
import MessageRightSidebar from '../components/MessageRightSidebar.vue'
import { getMessages, dealMessages, markAllAsRead as apiMarkAllAsRead } from '../services/messages'
import { globalState, invalidateMessages } from '../store'

const route = useRoute()

// 定义消息分类
const tabs = [
  { id: 'all', label: 'All Messages' },
  { id: 'system', label: 'System', icon: Info },
  { id: 'product', label: 'Product Updates', icon: Cpu },
  { id: 'security', label: 'Security', icon: ShieldAlert },
  { id: 'alert', label: 'Alerts', icon: AlertTriangle },
  { id: 'service', label: 'Service', icon: Activity }
]

const messages = ref<any[]>([])
const loading = ref(false)
const totalCount = ref(0)
const limit = ref(30)
const offset = ref(0)

const currentCategory = computed(() => {
    return (route.query.category as string) || 'all'
})

const filteredMessages = computed(() => messages.value)

const hasPrevious = computed(() => offset.value > 0)
const hasNext = computed(() => offset.value + messages.value.length < totalCount.value)

const fetchMessages = async () => {
    loading.value = true
    try {
        const res = await getMessages(currentCategory.value, limit.value, offset.value)
        const payload = dealMessages(res)
        messages.value = payload.results
        totalCount.value = payload.count
    } catch (e) {
        console.error('Failed to fetch messages', e)
    } finally {
        loading.value = false
    }
}

watch(() => route.query.category, () => {
    offset.value = 0
    fetchMessages()
})

onMounted(() => {
    fetchMessages()
})

const handleMarkAllAsRead = async () => {
    try {
        await apiMarkAllAsRead()
        messages.value.forEach(m => m.isRead = true)
        invalidateMessages()
    } catch (e) {
        console.error('Failed to mark all as read', e)
    }
}

// Refresh when other components signal that message read-state changed.
watch(() => globalState.messagesVersion, () => {
    fetchMessages()
})

const goPreviousPage = async () => {
    if (!hasPrevious.value) return
    offset.value = Math.max(0, offset.value - limit.value)
    await fetchMessages()
}

const goNextPage = async () => {
    if (!hasNext.value) return
    offset.value += limit.value
    await fetchMessages()
}

// 辅助方法：获取类别图标与颜色
const getCategoryIndicator = (category: string, severity: string) => {
    const map: Record<string, any> = {
        'system': { icon: Info, bg: 'bg-blue-50', text: 'text-blue-500' },
        'security': { icon: ShieldAlert, bg: 'bg-indigo-50', text: 'text-indigo-500' },
        'alert': { icon: AlertTriangle, bg: 'bg-rose-50', text: 'text-rose-500' },
        'product': { icon: Cpu, bg: 'bg-emerald-50', text: 'text-emerald-500' },
        'service': { icon: Activity, bg: 'bg-purple-50', text: 'text-purple-500' }
    }
    
    // 如果是严重的错误或警告，颜色直接使用警示色
    if (severity === 'error') {
        return { icon: AlertTriangle, bg: 'bg-rose-50', text: 'text-rose-500' }
    }
    if (severity === 'warning') {
        return { icon: ShieldAlert, bg: 'bg-amber-50', text: 'text-amber-500' }
    }
    
    return map[category] || { icon: Bell, bg: 'bg-slate-100', text: 'text-slate-500' }
}

const getCategoryName = (category: string) => {
    const found = tabs.find(t => t.id === category)
    return found ? found.label : category
}
</script>

<template>
<div class="min-h-screen bg-slate-50 flex flex-col font-sans">
    <NavBar />
    <main class="max-w-[1600px] w-full mx-auto p-6 flex flex-col lg:flex-row gap-6 flex-1">
        <MessageSidebar />
  <!-- 主内容区: 消息列表 -->
  <section class="flex-1 flex flex-col w-full min-w-0">
      <div class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden flex flex-col flex-1 h-full min-h-[600px]">
          
          <!-- 头部: 标题与说明 -->
          <div class="px-8 pt-8 pb-6 border-b border-slate-100 flex flex-col md:flex-row md:items-end justify-between gap-4 bg-white">
              <div>
                  <h1 class="text-2xl font-bold text-slate-800 tracking-tight flex items-center gap-3 mb-1">
                      Inbox
                      <span v-if="messages.filter(m => !m.isRead).length > 0" class="px-2 py-0.5 bg-primary/10 text-primary text-xs font-bold rounded-full border border-primary/20">
                          {{ messages.filter(m => !m.isRead).length }} New
                      </span>
                      <span v-if="loading" class="text-xs text-slate-400 font-normal">Loading...</span>
                  </h1>
                  <p class="text-[13px] text-slate-500">Manage all your notifications and system alerts.</p>
              </div>
              
              <!-- 右侧: 搜索框 (补齐视觉平衡) -->
              <div class="relative w-full md:w-64">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Search class="h-4 w-4 text-slate-400" />
                  </div>
                  <input 
                      type="text" 
                      class="block w-full pl-9 pr-3 py-1.5 border border-slate-200 rounded-lg leading-5 bg-slate-50 hover:bg-white text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary sm:text-sm transition-all shadow-sm"
                      placeholder="Search messages..."
                  />
              </div>
          </div>

          <!-- 消息列表 -->
          <div class="flex-1 flex flex-col overflow-y-auto">
              <div v-if="filteredMessages.length === 0" class="flex-1 flex flex-col items-center justify-center p-12 text-center text-slate-500">
                  <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4 border border-slate-100">
                      <Bell class="w-6 h-6 text-slate-400 opacity-50" />
                  </div>
                  <p class="text-base font-medium text-slate-700">No messages found</p>
                  <p class="text-sm mt-1">You're all caught up in this category.</p>
              </div>

              <!-- 列表内容 -->
                <div v-else class="divide-y divide-slate-100/60">
                    <router-link 
                        v-for="msg in filteredMessages" 
                        :key="msg.id" 
                        :to="`/messages/${msg.id}`"
                        class="group block transition-colors relative overflow-hidden bg-white hover:bg-slate-50/70 p-6"
                    >
                          <div class="flex gap-4 md:gap-5">
                              <!-- 分类图标容器 -->
                              <div class="flex-shrink-0 self-start w-11 h-11 rounded-full flex items-center justify-center border-2 border-white shadow-[0_2px_6px_rgba(0,0,0,0.04)]" :class="getCategoryIndicator(msg.category, msg.severity).bg">
                                <component :is="getCategoryIndicator(msg.category, msg.severity).icon" class="w-5 h-5" :class="getCategoryIndicator(msg.category, msg.severity).text" />
                            </div>

                            <!-- 核心内容 -->
                            <div class="flex-1 min-w-0 pr-8">
                                <div class="flex flex-col md:flex-row md:items-center gap-1.5 md:gap-3 mb-1.5">
                                    <h3 class="text-[15px] truncate transition-colors tracking-tight" :class="msg.isRead ? 'text-slate-500 font-medium' : 'text-slate-900 font-bold'">
                                        {{ msg.title }}
                                    </h3>
                                    <span class="hidden md:inline-block px-2 py-0.5 rounded-md bg-slate-100 text-slate-500 text-[10px] font-semibold uppercase tracking-widest border border-slate-200/50">
                                        {{ getCategoryName(msg.category) }}
                                    </span>
                                </div>
                                <p class="text-sm leading-relaxed line-clamp-2 md:pr-10 transition-colors" :class="msg.isRead ? 'text-slate-400 font-normal' : 'text-slate-500 font-medium'">
                                    {{ msg.content }}
                                </p>
                                <div class="mt-3 flex items-center gap-3 text-[11px] font-medium transition-colors" :class="msg.isRead ? 'text-slate-400/80' : 'text-slate-400'">
                                      <span>{{ msg.date }}</span>
                                      <div class="w-1 h-1 rounded-full bg-slate-300 md:hidden"></div>
                                      <span class="md:hidden text-primary">{{ getCategoryName(msg.category) }}</span>
                                  </div>
                              </div>

                              <!-- 进入详情的箭头 (Hover 显示) -->
                              <div class="absolute right-6 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all duration-200">
                                  <ChevronRight class="w-5 h-5 text-slate-400" />
                              </div>
                          </div>
                      </router-link>
              </div>
          </div>

          <!-- 底部快速栏 -->
          <div class="p-4 border-t border-slate-100 bg-slate-50/50 flex justify-between items-center text-xs text-slate-500 mt-auto">
              <div class="flex items-center gap-4">
                  <span>Showing {{ filteredMessages.length }} of {{ totalCount }} messages</span>
                  <button class="disabled:text-slate-300" :disabled="!hasPrevious" @click="goPreviousPage">Previous</button>
                  <button class="disabled:text-slate-300" :disabled="!hasNext" @click="goNextPage">Next</button>
              </div>
              <router-link to="/messages/preferences" class="font-medium text-primary hover:text-primary-700 transition-colors">Message Preferences</router-link>
          </div>
      </div>
  </section>

  <!-- 右侧侧边栏 (Sidebar) -->
  <MessageRightSidebar @mark-all-read="fetchMessages" />
    </main>
</div>
</template>

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
