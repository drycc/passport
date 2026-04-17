<template>
    <div id="ui-slide-panels">
        <div class="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center sm:justify-end">
            <div class="m-3 w-full max-w-lg bg-white rounded-xl shadow-xl flex flex-col overflow-hidden" >
                <div class="flex items-center justify-between px-6 py-4 border-b border-slate-200">
                    <div class="text-lg font-semibold text-slate-800" >
                        Delete Token
                    </div>
                    <button @click="canelDelete" class="p-2 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors" type="button">
                        <svg style="height: 16px; width: 16px;" class="w-5 h-5 fill-current" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1158" width="200" height="200"><path d="M574.55 522.35L904.4 192.5c16.65-16.65 16.65-44.1 0-60.75l-1.8-1.8c-16.65-16.65-44.1-16.65-60.75 0L512 460.25l-329.85-330.3c-16.65-16.65-44.1-16.65-60.75 0l-1.8 1.8c-17.1 16.65-17.1 44.1 0 60.75l329.85 329.85L119.6 852.2c-16.65 16.65-16.65 44.1 0 60.75l1.8 1.8c16.65 16.65 44.1 16.65 60.75 0L512 584.9l329.85 329.85c16.65 16.65 44.1 16.65 60.75 0l1.8-1.8c16.65-16.65 16.65-44.1 0-60.75L574.55 522.35z" p-id="1159"></path></svg>
                    </button>
                </div>

                <div class="p-6">
                    <div class="ui-modal-body">
                        <div class="ui-modal-message-wrap">
                            <div>
                                <div>
                                    <div>
                                        <div>
                                            <div>
                                                <div>
                                                    <label class="block text-base font-medium text-slate-800 mb-6">Are you sure you want to delete the access token:
                                                      <span class="font-mono text-sm text-slate-500 break-all bg-slate-100 px-2 py-1 rounded">{{ (token as any)?.token }}</span>?
                                                    </label>
                                                    <div>
                                                        <div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex items-center gap-3 px-6 py-4 border-t border-slate-200 bg-slate-50">
                    <button @click="canelDelete" class="flex-1 inline-flex justify-center items-center px-4 py-2 bg-white text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 font-medium transition-colors" type="button">Cancel</button>
                    <button @click="deleteToken" class="flex-1 inline-flex justify-center items-center px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-600 font-medium transition-colors" type="submit">Yes</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { reactive, toRefs } from 'vue'
const ElMessage = { success: alert, error: alert };
import {deleteAccessToken} from "../services/tokens";

export default {
    name: "AccessTokenDelete",
    props: {
        token: [Object, Function],
    },
    setup(props, context) {
        const state = reactive({
            token: props.token,
        })

        const canelDelete = () => {
            context.emit('closeDelete', { hasAccessTokenDeleted: false })
        }

        const deleteToken = () => {
            if (!state.token || typeof state.token === 'function' || !state.token.id) return;
            deleteAccessToken(state.token.id).then(res=>{
                if (res.status == 204) {
                    ElMessage.success("OK")
                    context.emit('closeDelete', { hasAccessTokenDeleted: true })
                }
            })
        }
        return {
            ...toRefs(state),
            canelDelete,
            deleteToken
        }
    }
}

</script>

<style scoped>
/* Tailwind handles styles */
</style>
