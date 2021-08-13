import axios from "../utils/axios";

export function getUser() {
    return axios.get(`/user/info/`)
}

export function dealUser(obj) {
    return {
        username: obj.data.username,
        email: obj.data.email,
    }
}

export function getCsrf() {
    return axios.get('/user/csrf/')
}

export function postLogout() {
    return axios.post(`/user/logout/`)
}

export function putAccount(data) {
    return axios.put(`/user/info/`, data)
}

export function putAccountPassword(data) {
    return axios.put(`/user/password/`, data)
}
