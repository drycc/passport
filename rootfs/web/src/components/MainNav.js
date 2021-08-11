import { reactive, toRefs} from 'vue'
import { useRouter } from 'vue-router'

export default {
    name: "MainNav",
    props: {
        isOverviewActive: {
            type: Boolean,
            default: false
        },
        isResourcesActive: {
            type: Boolean,
            default: false
        },
        isAccessActive: {
            type: Boolean,
            default: false
        },
        isActivityActive: {
            type: Boolean,
            default: false
        },
        isDeployActive: {
            type: Boolean,
            default: false
        },
        isMetricsActive: {
            type: Boolean,
            default: false
        },
        isSettingsActive: {
            type: Boolean,
            default: false
        },
        appDetail: [Object, Function]
    },
    setup(props) {
        const router = useRouter()
        const goToAppDetail = () => {
            router.push({ path: `/apps/${props.appDetail.id}` })
        }

        const goToResources = () => {
            router.push({ path: `/apps/${props.appDetail.id}/resources` })
        }

        const goToAccess = () => {
            router.push({ path: `/apps/${props.appDetail.id}/access` })
        }

        const goToActivity = () => {
            router.push({ path: `/apps/${props.appDetail.id}/activity` })
        }

        const goToDeploy = () => {
            router.push({ path: `/apps/${props.appDetail.id}/deploy` })
        }

        const goToMetrics = () => {
            router.push({ path: `/apps/${props.appDetail.id}/metrics` })
        }

        const goToSettings = () => {
            router.push({ path: `/apps/${props.appDetail.id}/settings` })
        }

        return {
            goToAppDetail,
            goToAccess,
            goToActivity,
            goToDeploy,
            goToMetrics,
            goToResources,
            goToSettings
        }
    },

}
