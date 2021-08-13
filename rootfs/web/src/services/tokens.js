import axios from "../utils/axios";

export function getAccessTokenList() {
    return axios.get(`/user/tokens/`)
}

export function dealAccessTokenList(obj) {
    return obj.data.map(item => {
        return {
            id: item.id,
            application: item.application,
            token: item.token,
            created: item.created,
            expires: item.expires
        }
    })
}

export function deleteAccessToken(id) {
    return axios.delete(`/user/tokens/` + id)
}