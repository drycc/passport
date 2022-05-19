import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

VUE_APP_BASE_URL = process.env.VUE_APP_BASE_URL ? process.env.VUE_APP_BASE_URL : ''

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    minify: true,
    chunkSizeWarningLimit: 3000
  },
  server:{
    proxy: { // 代理配置
      '/avatar': {
        target: VUE_APP_BASE_URL,
        changeOrigin: true,
      },
      '/user': {
        target: VUE_APP_BASE_URL,
        changeOrigin: true,
      },
      '/assets': {
        target: VUE_APP_BASE_URL,
        changeOrigin: true,
      },
      '/settings': {
        target: VUE_APP_BASE_URL,
        changeOrigin: true,
      },
    },
  },
  define: {
    'process.env': {
      VUE_APP_BASE_URL: VUE_APP_BASE_URL,
    },
  }
})
