import NavMenu from "./NavMenu.vue";
import UserMenu from "./UserMenu.vue";

export default {
    name: "NavBar",
    props: {
        user: {
            type: Object,
            default: null
        }
    },
    components: {
        'nav-menu': NavMenu,
        'user-menu': UserMenu
    }
}
