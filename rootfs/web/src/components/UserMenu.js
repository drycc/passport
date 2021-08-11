import {onMounted, reactive, toRefs} from "vue";
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
        const state = reactive({
            user :{
                username: null,
                email: null,
                is_superuser: null
            },
            isHiddenAdmin: true,
            adminUrl: ''
        })
        const logout = () => {
            postLogout().then(res=>{
                localStorage.clear()
                if (res.status == 302) {
                    router.push({ path: '/'})
                }
            })
            location.reload(true)
        }
        onMounted(async () => {
            var currentUser = sessionStorage.getItem('user')
            if (currentUser){
                state.user = JSON.parse(currentUser)
            }else {
                // const res = await getUser()
                const res = ''
                state.user = dealUser(res)
                if (state.user){
                    sessionStorage.setItem('user', JSON.stringify(state.user))
                }
            }

            if (state.user.is_superuser){
                state.isHiddenAdmin = false
            }
            state.adminUrl = process.env.NODE_ENV == 'development' ? 'http://d.uucin.com/admin/' : 'http://d.uucin.com/admin/'
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
