<template>
    <footer class="mt-auto py-8">
        <div class="max-w-[1600px] mx-auto px-6 w-full">
            <div v-if="legalEnabled" class="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-xs text-slate-500">
                <span class="text-slate-400">© {{year}} drycc.com</span>
                <a class="hover:text-primary transition-colors" href="https://legal.doopai.com/#/cloud-services-terms" target="_blank" rel="noopener noreferrer">Terms</a>
                <a class="hover:text-primary transition-colors" href="https://legal.doopai.com/#/doopai-privacy-policy" target="_blank" rel="noopener noreferrer">Privacy</a>
                <a class="hover:text-primary transition-colors" href="https://github.com/drycc" target="_blank" rel="noopener noreferrer">Open Source</a>
                <a class="hover:text-primary transition-colors" href="https://drycc.slack.com/" target="_blank" rel="noopener noreferrer">Community</a>
                <a class="hover:text-primary transition-colors" href="https://www.drycc.cc/" target="_blank" rel="noopener noreferrer">Documentation</a>
                <a class="hover:text-primary transition-colors" href="https://tawk.to/chat/6234b5491ffac05b1d7f4669/1fueu8a9t" target="_blank" rel="noopener noreferrer">Support</a>
            </div>
            
            <div v-else class="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-xs text-slate-500">
                <span class="text-slate-400">© {{year}} drycc.cc</span>
                <a class="hover:text-primary transition-colors" href="https://github.com/drycc" target="_blank" rel="noopener noreferrer">Open Source</a>
                <a class="hover:text-primary transition-colors" href="https://drycc.slack.com/" target="_blank" rel="noopener noreferrer">Community</a>
                <a class="hover:text-primary transition-colors" href="https://www.drycc.cc/" target="_blank" rel="noopener noreferrer">Documentation</a>
                <a class="hover:text-primary transition-colors" href="https://tawk.to/chat/6234b5491ffac05b1d7f4669/1fueu8a9t" target="_blank" rel="noopener noreferrer">Support</a>
                <a class="hover:text-primary transition-colors" href="https://github.com/drycc/workflow/issues" target="_blank" rel="noopener noreferrer">Issues</a>
            </div>
        </div>
    </footer>
</template>

<script lang="ts">
import {toRefs, reactive, onMounted} from 'vue'

import { getSettings } from '../services/settings'

export default {
    name: "Footer",
    setup(props) {
        const state = reactive({
            year: new Date().getFullYear(),
            legalEnabled: false,
        })
        onMounted(async () => {
            var res =  await getSettings()
            state.legalEnabled = res.data.legal
        })
        return {
            ...toRefs(state),
        }
    },

}

</script>
<style scoped>
/* Scoped styles removed */
</style>