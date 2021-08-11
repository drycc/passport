import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import {onBeforeMount, reactive, toRefs} from 'vue'
import {dealAccessTokenList, getAccessTokenList} from "../services/tokens";
import {getCsrf} from "../services/user";

export default {
    name: "AccessTokenList",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
    },
    setup() {
        const state = reactive({
            tokens: [],
        })

        const localStorageInit = () => {
            getCsrf().then(res=>{
                sessionStorage.setItem('csrftoken', res.data.token)
            })
        }

        onBeforeMount(async () => {
            state.tokens = []
            // localStorageInit()
            // let res = await getAccessTokenList()
            // state.tokens = res.data && res.data.results ? dealAccessTokenList(res) : []
        })

        return {
            ...toRefs(state),
        }
    },
}
