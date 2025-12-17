import { createRouter, createWebHistory } from 'vue-router'
import AccessTokenList from "../views/AccessTokenList.vue";
import AccountSetting from "../views/AccountSetting.vue";
import Organizations from "../views/Organizations.vue";


const routes = [
    {
        path: '/',
        redirect: '/access-tokens',
    },
    {
        path: '/access-tokens',
        name: 'AccessTokenList',
        component: AccessTokenList
    },
    {
        path: '/account-setting',
        name: 'AccountSetting',
        component: AccountSetting
    },
    {
        path: '/organizations',
        name: 'Organizations',
        component: Organizations
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
