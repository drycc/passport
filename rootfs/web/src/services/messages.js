import axios from "../utils/axios";

export function getMessages(category, limit = 30, offset = 0) {
    const params = { limit, offset };
    if (category && category !== 'all') {
        params.category = category;
    }
    return axios.get(`/user/messages/`, { params })
}

export function dealMessages(obj) {
    return {
        count: obj.data.count,
        next: obj.data.next,
        previous: obj.data.previous,
        results: obj.data.results.map(item => {
            return {
                id: item.id,
                category: item.category,
                title: item.title,
                content: item.content,
                date: item.date,
                isRead: item.is_read,
                severity: item.severity
            }
        })
    }
}

export function getMessageDetail(id) {
    return axios.get(`/user/messages/` + id)
}

export function dealMessageDetail(obj) {
    const item = obj.data;
    return {
        id: item.id,
        category: item.category,
        title: item.title,
        fullContent: item.full_content || item.content,
        date: item.date,
        isRead: item.is_read,
        severity: item.severity,
        actionLink: item.action_link,
        actionText: item.action_text
    }
}

export function markAllAsRead() {
    return axios.put(`/user/messages/mark-all-read/`)
}

export function getMessagePreferences() {
    return axios.get(`/user/message-preferences/`)
}

export function updateMessagePreferences(data) {
    return axios.put(`/user/message-preferences/`, data)
}
