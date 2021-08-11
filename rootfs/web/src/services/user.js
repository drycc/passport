import axios from "../utils/axios";

export function getUser() {
    return axios.get(`/api/users/`)
}

export function dealUser(obj) {
    return {
        username: obj.data.username,
        email: obj.data.email,
    }
}

export function getCsrf() {
    return axios.get('/api/user/csrf/')
}

export function postLogout() {
    return axios.post(`/api/user/logout/`)
}
