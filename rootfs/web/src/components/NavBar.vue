<!--导航栏-->
<template>
  <header class="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm w-full">
    <div class="max-w-[1600px] w-full mx-auto flex items-center justify-between px-6 py-2.5 h-14">
      <!-- Logo -->
      <div class="flex items-center">
          <a href="/" class="flex items-center gap-2.5 hover:opacity-80 transition-opacity">
              <div class="flex items-center justify-center w-8 h-8 bg-primary rounded shadow-sm">
                  <img class="w-5 h-5 object-contain filter brightness-0 invert" src="../../src/assets/icons/drycc.svg" alt="Drycc" />
              </div>
              <span class="text-base font-semibold text-slate-800 tracking-tight">Drycc CaaS</span>
          </a>
      </div>
      
      <!-- 右侧导航与工具栏合并 -->
      <div class="flex items-center gap-6 -mr-3">
          <div class="hidden lg:flex items-center text-sm font-medium text-slate-600">
              <nav-menu />
          </div>
          <div class="flex items-center text-slate-500">
              <user-menu :user="user" />
          </div>
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import NavMenu from "./NavMenu.vue";
import UserMenu from "./UserMenu.vue";

export default {
    name: "NavBar",
    props: {
        user: {
            type: Object,
            default: null
        }
    },
    components: {
        'nav-menu': NavMenu,
        'user-menu': UserMenu
    }
}

</script>

<style scoped>
/* Scoped styles removed */
</style>
