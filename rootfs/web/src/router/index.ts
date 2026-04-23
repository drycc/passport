import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import AccessTokenList from "../views/AccessTokenList.vue";
import AccountSetting from "../views/AccountSetting.vue";


const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Overview',
        component: () => import('../views/Overview.vue')
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
        path: '/messages',
        name: 'messages',
        component: () => import('../views/MessageList.vue')
    },
    {
        path: '/messages/preferences',
        name: 'message-preferences',
        component: () => import('../views/MessagePreferences.vue')
    },
    {
        path: '/messages/:id',
        name: 'message-detail',
        component: () => import('../views/MessageDetail.vue'),
        props: true
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
