import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

const VUE_APP_BASE_URL = process.env.VUE_APP_BASE_URL || "";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  build: {
    minify: true,
    chunkSizeWarningLimit: 3000,
  },
  server: {
    proxy: {
      "/avatar": { target: VUE_APP_BASE_URL, changeOrigin: false, xfwd: true },
      "/orgs": { target: VUE_APP_BASE_URL, changeOrigin: false, xfwd: true },
      "/user": { target: VUE_APP_BASE_URL, changeOrigin: false, xfwd: true },
      "/auth": { target: VUE_APP_BASE_URL, changeOrigin: false, xfwd: true },
      "/oauth": { target: VUE_APP_BASE_URL, changeOrigin: false, xfwd: true },
      "/assets": { target: VUE_APP_BASE_URL, changeOrigin: false, xfwd: true },
      "/settings": { target: VUE_APP_BASE_URL, changeOrigin: false, xfwd: true }
    },
  },
  define: {
    "process.env.VUE_APP_BASE_URL": JSON.stringify(VUE_APP_BASE_URL),
  },
});
