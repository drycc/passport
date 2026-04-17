import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import AccessTokenList from "../views/AccessTokenList.vue";
import AccountSetting from "../views/AccountSetting.vue";


const routes: Array<RouteRecordRaw> = [
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
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
