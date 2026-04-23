import { reactive } from 'vue'
import { getSettings } from './services/settings'

export const globalState = reactive({
    dashboardUrl: '/',
    contactSupportUrl: 'https://community.drycc.cc/',
    settingsLoaded: false,
    // Bumped whenever the user's message read-state changes (e.g. mark-all-read,
    // mark single message as read). Components that display messages should
    // watch this value and refresh their local state.
    messagesVersion: 0,
})

/** Notify all message-aware components to refresh. */
export const invalidateMessages = () => {
    globalState.messagesVersion += 1
}

export const fetchGlobalSettings = async () => {
    if (globalState.settingsLoaded) return;
    try {
        const res = await getSettings()
        if (res.data) {
            if (res.data.dashboard_url) globalState.dashboardUrl = res.data.dashboard_url
            if (res.data.contact_support_url) globalState.contactSupportUrl = res.data.contact_support_url
        }
        globalState.settingsLoaded = true
    } catch (e) {
        console.error("Failed to fetch settings", e)
    }
}
