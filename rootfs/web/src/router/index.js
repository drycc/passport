import { createRouter, createWebHistory } from 'vue-router'
import AccessTokenList from "../views/AccessTokenList.vue";


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
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
