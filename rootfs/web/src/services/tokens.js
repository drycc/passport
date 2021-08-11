import axios from "../utils/axios";

export function getAccessTokenList() {
    return axios.get(`/api/tokens/`)
}

export function dealAccessTokenList(obj) {
    return obj.data.results.map(item => {
        return {
            id: item.id,
            name: item.name,
            authorization_grant_type: item.authorization_grant_type,
            user: item.user,
            created: item.created
        }
    })
}
