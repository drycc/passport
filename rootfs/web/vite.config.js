import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

VUE_APP_BASE_URL = process.env.VUE_APP_BASE_URL
  ? process.env.VUE_APP_BASE_URL
  : "";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    minify: true,
    chunkSizeWarningLimit: 3000,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('element-plus')) {
            return 'element-plus';
          }
        },
      },
    },
  },
  server: {
    proxy: {
      // 代理配置
      "/avatar": {
        target: VUE_APP_BASE_URL,
        changeOrigin: false,
        xfwd: true,
      },
      "/orgs": {
        target: VUE_APP_BASE_URL,
        changeOrigin: false,
        xfwd: true,
      },
      "/user": {
        target: VUE_APP_BASE_URL,
        changeOrigin: false,
        xfwd: true,
      },
      "/auth": {
        target: VUE_APP_BASE_URL,
        changeOrigin: false,
        xfwd: true,
      },
      "/oauth": {
        target: VUE_APP_BASE_URL,
        changeOrigin: false,
        xfwd: true,
      },
      "/assets": {
        target: VUE_APP_BASE_URL,
        changeOrigin: false,
        xfwd: true,
      },
      "/settings": {
        target: VUE_APP_BASE_URL,
        changeOrigin: false,
        xfwd: true,
      },
    },
  },
  define: {
    "process.env": {
      VUE_APP_BASE_URL: VUE_APP_BASE_URL,
    },
  },
});
