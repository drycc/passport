import {toRefs, reactive} from 'vue'

export default {
    name: "Footer",
    setup(props) {
        const state = reactive({
            year: new Date().getFullYear(),
            legalEnabled: false,
        })
        state.legalEnabled = process.env.VUE_APP_LEGAL_ENABLED == "true" ? true : false;
        return {
            ...toRefs(state),
        }
    },

}
