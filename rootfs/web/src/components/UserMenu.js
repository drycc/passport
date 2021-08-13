import {onMounted, reactive, toRefs} from "vue";
import { useRouter } from 'vue-router'
import {dealUser, getUser, postLogout} from "../services/user";

export default {
    name: "UserMenu",
    data() {
        return {
            isMenuActived: false
        }
    },
    methods: {
        openOrCloseMenu() {
            this.isMenuActived = !this.isMenuActived;
        }
    },
    setup() {
        const router = useRouter()
        const state = reactive({
            user :{
                username: null,
                email: null,
                is_superuser: null
            },
        })
        const logout = () => {
            postLogout().then(res=>{
                if (res.status == 200) {
                    sessionStorage.clear()
                    router.push({ path: '/'})
                }
            })
            location.reload(true)
        }
        onMounted(async () => {
            let user = sessionStorage.getItem('user')
            if (user){
                state.user = JSON.parse(user)
            }else {
                const res = await getUser()
                state.user = dealUser(res)
                if (state.user){
                    sessionStorage.setItem('user', JSON.stringify(state.user))
                }
            }
        })

        return {
            ...toRefs(state),
            logout
        }
    },
    mounted() {
        let _this = this
        document.addEventListener('click', function (e) {
            // 下面这句代码是获取 点击的区域是否包含你的菜单，如果包含，说明点击的是菜单以外，不包含则为菜单以内
            if (e.target.id !== 'menu-account') {
                _this.isMenuActived = false
            }
        })
    }
}
