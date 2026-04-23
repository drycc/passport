<template>
    <ul id="menu-navigator" class="flex flex-wrap items-center justify-center gap-1 list-none m-0 p-0 text-sm font-medium">
        <li class="relative">
            <a class="flex items-center gap-1.5 px-2.5 py-1.5 text-sm font-medium text-slate-700 bg-white border border-transparent rounded-lg hover:bg-slate-50 transition-all focus:outline-none group" :href="globalState.dashboardUrl">
                <LayoutGrid class="w-4 h-4 text-primary" aria-hidden="true" />
                <span>Dashboard</span>
            </a>
        </li>
        <li class="relative hidden md:block">
            <a class="flex items-center gap-1.5 px-2.5 py-1.5 text-sm font-medium text-slate-700 bg-white border border-transparent rounded-lg hover:bg-slate-50 transition-all focus:outline-none group" href="https://www.drycc.cc/zh-cn/docs/roadmap/" target="_blank" rel="noopener noreferrer">
                <Zap class="w-4 h-4 text-primary opacity-80" aria-hidden="true" />
                <span>What's New</span>
            </a>
        </li>
        <li class="relative">
            <dropdown
                trigger-id="menu-nav"
                menu-id="ui-nav-menu-resources"
                trigger-label="Resources"
                :trigger-icon="resourcesTriggerIcon"
                :items="resourceItems"
                :menu-width="226"
            >
                <template #trigger>
                    <button class="flex items-center gap-1.5 px-2.5 py-1.5 text-sm font-medium text-slate-700 bg-white border border-transparent rounded-lg hover:bg-slate-50 transition-all focus:outline-none group" type="button">
                        <component class="w-4 h-4 text-primary opacity-80" aria-hidden="true" :is="resourcesTriggerIcon" />
                        <span>Resources</span>
                    </button>
                </template>
            </dropdown>
        </li>
    </ul>
</template>

<script lang="ts">
import { markRaw } from "vue";
import { MessageSquare, FileText, Bookmark, BookOpen, LayoutGrid, Zap } from "lucide-vue-next";
import Dropdown from "./Dropdown.vue";
import { globalState } from "../store";

export default {
    name: "NavMenu",
    components: { LayoutGrid, Zap, Dropdown },
    setup() {
        return { globalState }
    },
    data() {
        return {
            isMenuActived: false,
            resourcesTriggerIcon: markRaw(Bookmark),
            resourceItems: [
                {
                    key: "docs",
                    label: "Documentation",
                    href: "https://www.drycc.cc/docs/",
                    icon: markRaw(FileText),
                    external: true
                },
                {
                    key: "community",
                    label: "Community Support",
                    href: "https://www.drycc.cc/community/",
                    icon: markRaw(MessageSquare),
                    external: true
                },
                {
                    key: "blog",
                    label: "Drycc.cc Blog",
                    href: "https://www.drycc.cc/blog/",
                    icon: markRaw(BookOpen),
                    external: true
                },
            ]
        }
    }
}

</script>

<style scoped>
/* Scoped styles removed */
</style>
