export default {
    name: "NavMenu",
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
    mounted() {
        let _this = this
        document.addEventListener('click', function (e) {
            // 下面这句代码是获取 点击的区域是否包含你的菜单，如果包含，说明点击的是菜单以外，不包含则为菜单以内
            if (e.target.id !== 'menu-nav') {
                _this.isMenuActived = false
            }

        })
    }
}
