import App from './App.vue'
import router from './router'
import { createApp } from 'vue'
import { i18n, setLang, getUAgentLang } from './lang'
import './styles/unified.css'

declare global {
  interface Date {
    format(format: string): string;
  }
}

/**
 * 时间对象的格式化;
 */
Date.prototype.format = function(format: string) {
    var o: Record<string, number> = {
        "M+" : this.getMonth() + 1,
        "d+" : this.getDate(),
        "h+" : this.getHours(),
        "m+" : this.getMinutes(),
        "s+" : this.getSeconds(),
        "q+" : Math.floor((this.getMonth() + 3) / 3),
        "S" : this.getMilliseconds()
    }

    if (/(y+)/.test(format)) {
        format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    }

    for (var k in o) {
        if (new RegExp("(" + k + ")").test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k].toString() : ("00" + o[k]).substr(("" + o[k]).length));
        }
    }
    return format;
}

// 初始化
function init () {
    // 语言初始化
    const lang = getUAgentLang()
    setLang(lang)
}

init()

const app = createApp(App)
app.use(router)
app.use(i18n)
app.mount('#app')
