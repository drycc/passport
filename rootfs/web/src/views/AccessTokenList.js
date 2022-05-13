import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import {onBeforeMount, reactive, toRefs} from 'vue'
import MainNav from "../components/MainNav.vue";
import MainFooter from "../components/MainFooter.vue";
import AccessTokenDelete from "../components/AccessTokenDelete.vue"

import {dealAccessTokenList, getAccessTokenList, deleteAccessToken} from "../services/tokens";

export default {
    name: "AccessTokenList",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-nav': MainNav,
        'main-footer': MainFooter,
        'access-token-delete': AccessTokenDelete
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
