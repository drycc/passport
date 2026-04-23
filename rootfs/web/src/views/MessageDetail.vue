<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import MessageSidebar from '../components/MessageSidebar.vue'
import { ArrowLeft, Bell, ShieldAlert, Cpu, Activity, Info, AlertTriangle, AlertCircle, Clock, ChevronRight } from 'lucide-vue-next'
import MessageRightSidebar from '../components/MessageRightSidebar.vue'
import { getMessageDetail, dealMessageDetail } from '../services/messages'

const route = useRoute()
const router = useRouter()
const messageId = route.params.id as string

const message = ref<any>(null)
const loading = ref(false)

onMounted(async () => {
    loading.value = true
    try {
        const res = await getMessageDetail(messageId)
        message.value = dealMessageDetail(res)
    } catch (e) {
        console.error('Failed to fetch message detail', e)
        message.value = {
            id: messageId,
            category: 'system',
            title: 'Message Details',
            fullContent: 'Failed to load message content.',
            date: '',
            severity: 'info'
        }
    } finally {
        loading.value = false
    }
})

// 强大的自定义解析器：不再依赖外部 prose 和容易变形的全局 css
const parsedContent = computed(() => {
    if (!message.value) return '';
    let text = message.value.fullContent;
    
    // 解析基础的 HTML 标签标记
    text = text.replace(/<b>(.*?)<\/b>/g, '<strong class="font-semibold text-slate-800">$1</strong>');
    text = text.replace(/<code>(.*?)<\/code>/g, '<code class="bg-rose-50 text-rose-600 px-1.5 py-0.5 rounded border border-rose-100/60 text-[0.85em] font-mono leading-none">$1</code>');
    
    const lines = text.split('\n');
    let html = '';
    let inList = false;
    
    lines.forEach((line) => {
        const trimmed = line.trim();
        if (trimmed.startsWith('•') || trimmed.startsWith('-')) {
            if (!inList) {
                // 开始无序列表，增加合适的上下外边距
                html += '<ul class="my-5 space-y-3.5">';
                inList = true;
            }
            const liText = trimmed.substring(1).trim();
            // 自定义完美的项目符号与对齐
            html += `<li class="flex items-start"><span class="mr-3 mt-2 inline-flex w-1.5 h-1.5 rounded-full bg-slate-300 flex-shrink-0"></span><span class="flex-1 leading-relaxed text-slate-600">${liText}</span></li>`;
        } else {
            if (inList) {
                html += '</ul>';
                inList = false;
            }
            if (trimmed === '') {
                // 空行转换为高度空隙
                html += '<div class="h-6"></div>'; 
            } else {
                // 普通段落
                html += `<div class="mb-1 leading-relaxed text-slate-600">${trimmed}</div>`;
            }
        }
    });
    
    if (inList) html += '</ul>';
    return html;
})

const getCategoryIndicator = (category: string, severity: string) => {
    const map: Record<string, any> = {
        'system': { icon: Info, bg: 'bg-blue-50', text: 'text-blue-600', ring: 'ring-blue-50/50', badgeBg: 'bg-blue-50', badgeBorder: 'border-blue-100/60' },
        'security': { icon: ShieldAlert, bg: 'bg-indigo-50', text: 'text-indigo-600', ring: 'ring-indigo-50/50', badgeBg: 'bg-indigo-50', badgeBorder: 'border-indigo-100/60' },
        'alert': { icon: AlertTriangle, bg: 'bg-rose-50', text: 'text-rose-600', ring: 'ring-rose-50/50', badgeBg: 'bg-rose-50', badgeBorder: 'border-rose-100/60' },
        'product': { icon: Cpu, bg: 'bg-emerald-50', text: 'text-emerald-600', ring: 'ring-emerald-50/50', badgeBg: 'bg-emerald-50', badgeBorder: 'border-emerald-100/60' },
        'service': { icon: Activity, bg: 'bg-purple-50', text: 'text-purple-600', ring: 'ring-purple-50/50', badgeBg: 'bg-purple-50', badgeBorder: 'border-purple-100/60' }
    }
    if (severity === 'error') return { icon: AlertCircle, bg: 'bg-rose-50', text: 'text-rose-600', ring: 'ring-rose-50/50', badgeBg: 'bg-rose-50', badgeBorder: 'border-rose-100/60' }
    if (severity === 'warning') return { icon: ShieldAlert, bg: 'bg-orange-50', text: 'text-orange-600', ring: 'ring-orange-50/50', badgeBg: 'bg-orange-50', badgeBorder: 'border-orange-100/60' } 
    return map[category] || { icon: Bell, bg: 'bg-slate-100', text: 'text-slate-600', ring: 'ring-slate-50', badgeBg: 'bg-slate-50', badgeBorder: 'border-slate-200' }
}
</script>

<template>
<div class="min-h-screen bg-slate-50 flex flex-col font-sans">
    <NavBar />
    <main class="max-w-[1600px] w-full mx-auto p-6 flex flex-col lg:flex-row gap-6 flex-1">
        <MessageSidebar />
  <!-- 主内容区 -->
  <section class="flex-1 flex flex-col w-full min-w-0">
      <div v-if="message" class="bg-white rounded-lg shadow-sm border border-slate-200 min-h-[600px] flex flex-col flex-1 overflow-hidden">
          
          <!-- 导航栏：极简模式 -->
          <div class="px-6 py-4 flex items-center border-b border-slate-100 bg-slate-50/40">
              <button @click="router.push('/messages')" class="inline-flex items-center text-sm font-medium text-slate-500 hover:text-slate-800 transition-colors focus:outline-none">
                  <ArrowLeft class="w-4 h-4 mr-2 text-slate-400" />
                  Back to Inbox
              </button>
          </div>

          <!-- 头部区域：突出视觉层级 -->
          <div class="px-8 md:px-12 pt-10 pb-8 border-b border-slate-100/80">
              <div class="flex items-start gap-4 md:gap-5">
                  <!-- 个性化图标容器 -->
                  <div class="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 ring-4 mt-0.5" 
                       :class="[getCategoryIndicator(message.category, message.severity).bg, getCategoryIndicator(message.category, message.severity).ring]">
                      <component :is="getCategoryIndicator(message.category, message.severity).icon" class="w-6 h-6" 
                                 :class="getCategoryIndicator(message.category, message.severity).text" />
                  </div>
                  
                  <!-- 文本分析区 -->
                  <div class="flex-1 w-full min-w-0">
                      <h1 class="text-xl md:text-[22px] font-bold text-slate-900 tracking-tight leading-tight mb-3">
                          {{ message.title }}
                      </h1>
                      
                      <div class="flex flex-wrap items-center gap-3 text-[11px] font-medium text-slate-500">
                          <span class="inline-flex items-center px-2 py-0.5 rounded border uppercase tracking-wider font-semibold"
                                :class="[getCategoryIndicator(message.category, message.severity).badgeBg, getCategoryIndicator(message.category, message.severity).badgeBorder, getCategoryIndicator(message.category, message.severity).text]">
                              {{ message.category }}
                          </span>
                          <span class="flex items-center gap-1.5 opacity-80">
                              <Clock class="w-3 h-3" />
                              {{ message.date }}
                          </span>
                      </div>
                  </div>
              </div>
          </div>

          <!-- 内容正文区 -->
          <div class="px-8 md:px-12 py-10 flex-1">
              <div class="max-w-3xl">
                  <!-- 正文 (直接嵌入经过智能解析后的 HTML) -->
                  <div class="text-[15px]" v-html="parsedContent"></div>

                  <!-- 行动按钮 (与正文自然连贯) -->
                  <div v-if="message.actionLink" class="mt-12">
                      <button class="inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-primary hover:bg-primary-600 text-white text-sm font-semibold rounded-lg shadow-sm transition-all focus:outline-none">
                          {{ message.actionText }}
                          <ChevronRight class="w-4 h-4 opacity-80" />
                      </button>
                  </div>
              </div>
          </div>
          
      </div>
  </section>

  <!-- 右侧侧边栏 (Sidebar) -->
  <MessageRightSidebar />
    </main>
</div>
</template>
