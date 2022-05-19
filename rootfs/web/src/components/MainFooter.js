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
