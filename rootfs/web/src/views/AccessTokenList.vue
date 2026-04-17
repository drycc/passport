<!--app列表页-->
<template>
<div class="min-h-screen bg-slate-50 flex flex-col font-sans" :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <main class="max-w-[1600px] w-full mx-auto p-6 flex flex-col lg:flex-row gap-6 flex-1">
        <main-nav :is-access-token-active="true"  />
        <section class="flex-1 flex flex-col">
            <access-token-delete ref="accessTokenDelete" v-if="isShowDelete"
              :token="token"
              @closeDelete="closeDelete"
            />
            
            <!-- Table Card -->
            <div class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden flex-1 flex flex-col min-h-[600px]">
                <!-- Header -->
                <div class="px-6 py-5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                        <h2 class="text-lg font-medium text-slate-800">Access Tokens</h2>
                        <p class="text-sm text-slate-500 mt-1">Generate and manage API tokens to authenticate with third-party integrations.</p>
                    </div>
                </div>

                <!-- Table Content -->
                <div class="w-full overflow-x-auto">
                    <table class="w-full text-left text-sm text-slate-600">
                        <thead class="bg-slate-50/50 border-b border-slate-200 text-slate-500 text-xs tracking-wider font-medium">
                            <tr>
                                <th class="px-6 py-4">Application</th>
                                <th class="px-6 py-4">Token</th>
                                <th class="px-6 py-4">Created</th>
                                <th class="px-6 py-4">Expires</th>
                                <th class="px-6 py-4 text-right w-16"></th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <tr v-for="(token, index) in tokens" :key="index" class="hover:bg-primary-50 transition-colors">
                                <td class="px-6 py-4 font-medium text-slate-800">{{ token.application }}</td>
                                <td class="px-6 py-4 font-mono text-xs text-slate-500 break-all">{{ token.token }}</td>
                                <td class="px-6 py-4 whitespace-nowrap">{{ token.created }}</td>
                                <td class="px-6 py-4 whitespace-nowrap">{{ token.expires }}</td>
                                <td class="px-6 py-4 text-right whitespace-nowrap">
                                  <button @click="showDelete(index)" class="text-slate-400 hover:text-red-600 hover:bg-red-50 p-2 rounded-md transition-colors" title="Delete token">
                                    <Trash2 class="w-4 h-4" />
                                  </button>
                                </td>
                            </tr>
                            <tr v-if="!tokens || tokens.length === 0">
                                <td colspan="5" class="px-6 py-16">
                                    <div class="flex flex-col items-center justify-center text-center">
                                        <div class="w-16 h-16 bg-slate-50 border border-slate-100 rounded-full flex items-center justify-center mb-4">
                                            <div class="w-10 h-10 border border-slate-200 bg-white rounded-full flex items-center justify-center shadow-sm">
                                                <div class="w-4 h-[2px] bg-slate-300 rounded-full"></div>
                                            </div>
                                        </div>
                                        <h3 class="text-lg font-medium text-slate-800 mb-1">No access tokens</h3>
                                        <p class="text-sm text-slate-500 max-w-sm">You haven't generated any access tokens yet. Create one via Drycc CLI to authenticate API requests.</p>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- Right Sidebar (Token Info & Help) -->
        <aside class="hidden xl:flex flex-col w-[280px] flex-shrink-0 gap-5">
            <!-- About Tokens -->
            <div class="bg-white rounded border border-slate-200 overflow-hidden">
                <div class="px-5 py-3.5 border-b border-slate-100 bg-white">
                    <h3 class="text-[13px] font-semibold text-slate-700">Security Guidance</h3>
                </div>
                <div class="p-5">
                    <p class="text-[12px] text-slate-500 leading-relaxed mb-4">
                        Treat your tokens like passwords. Never share them or hardcode them directly into your application source code.
                    </p>
                   <a href="https://oauth.net/security/" target="_blank" class="text-[12px] font-medium text-primary hover:text-primary-600 flex items-center gap-1 transition-colors">
                        Learn more about SSO
                    </a>
                </div>
            </div>

            <!-- Need Help? -->
            <div class="bg-white rounded border border-slate-200 overflow-hidden">
                <div class="px-5 py-3.5 border-b border-slate-100 bg-white">
                    <h3 class="text-[13px] font-semibold text-slate-700">Need Help?</h3>
                </div>
                <div class="p-0">
                    <ul class="divide-y divide-slate-100">
                        <li>
                            <a href="https://www.drycc.cc" target="_blank" rel="noopener noreferrer" class="px-5 py-3 text-[12px] text-slate-600 hover:text-slate-900 hover:bg-slate-50 flex items-center justify-between transition-colors w-full">
                                <span>API Documentation</span>
                                <i data-lucide="external-link" class="w-3.5 h-3.5 text-slate-400"></i>
                            </a>
                        </li>
                        <li>
                            <a href="https://drycc.slack.com/" target="_blank" rel="noopener noreferrer" class="px-5 py-3 text-[12px] text-slate-600 hover:text-slate-900 hover:bg-slate-50 flex items-center justify-between transition-colors w-full">
                                <span>Community Support</span>
                                <i data-lucide="external-link" class="w-3.5 h-3.5 text-slate-400"></i>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </aside>
    </main>
    <main-footer />
</div>
</template>

<script lang="ts">
import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import {onBeforeMount, reactive, toRefs} from 'vue'
import MainNav from "../components/MainNav.vue";
import MainFooter from "../components/MainFooter.vue";
import AccessTokenDelete from "../components/AccessTokenDelete.vue"
import { Trash2 } from "lucide-vue-next"

import {dealAccessTokenList, getAccessTokenList, deleteAccessToken} from "../services/tokens";

export default {
    name: "AccessTokenList",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-nav': MainNav,
        'main-footer': MainFooter,
        'access-token-delete': AccessTokenDelete,
        Trash2
    },
    setup() {
        const state = reactive({
            tokens: [],
            token: Object,
            isShowDelete: false,
        })

        onBeforeMount(async () => {
            await fetchAccessTokenList()
        })

        const fetchAccessTokenList = (async () => {
            let res = await getAccessTokenList()
            state.tokens = res.data ? dealAccessTokenList(res) : []
        })

        const showDelete = (index) => {
            state.isShowDelete = true
            state.token = state.tokens.slice(index, index + 1)[0];
        }

        const closeDelete = (param) => {
            state.isShowDelete = false
            if (param.hasAccessTokenDeleted) {
                fetchAccessTokenList()
            }
        }

        return {
            ...toRefs(state),
            showDelete,
            closeDelete
        }
    },
}

</script>

<style scoped>
/* Styles removed in favor of Tailwind CSS framework classes */
</style>
