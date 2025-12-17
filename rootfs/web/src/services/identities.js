import axios from "../utils/axios";

export const getIdentityProviders = () => {
    return axios.get('/user/identity-providers/')
}

export const getLinkedIdentities = () => {
    return axios.get('/user/identities/')
}

export const unlinkIdentity = (identityId) => {
    return axios.delete(`/user/identities/${identityId}`)
}

export const getOAuthPending = () => {
    return axios.get('/user/oauth/pending/')
}

export const createOAuthUser = (payload) => {
    return axios.post('/user/oauth/create/', payload)
}