import axios from "../utils/axios";

export function getSettings() {
    return axios.get(`/settings/`)
}