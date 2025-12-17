<template>
    <nav class="app-nav nav nav-tabs sub-nav ember-view">
        <div class="limit-width">
            <div class="sub-nav-item ember-view">
                <a @click="goToAccessToken" class="ember-view" :class="{'active': isAccessTokenActive}">
                    <svg style="height: 24px; width: 24px;"  class="icon malibu-icon fill-purple" >
                        <title id="malibu-icon-ember486">Access Tokens</title>
                        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#overview-28"></use>
                    </svg>
                    <span class="sub-nav-item-name gray">Access Tokens</span>
                </a>
            </div>
            <div class="sub-nav-item ember-view">
                <a @click="goToAccountSetting" class="ember-view" :class="{'active': isAccountSettingActive}">
                    <svg style="height: 24px; width: 24px;" class="icon malibu-icon fill-gray" >
                        <title id="malibu-icon-ember489">Account Setting</title>
                        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#formation-28"></use>
                    </svg>
                    <span class="sub-nav-item-name gray">Account Setting</span>
                </a>
            </div>
            <div class="sub-nav-item ember-view">
                <a @click="goToOrganizations" class="ember-view" :class="{'active': isOrganizationsActive}">
                    <svg style="height: 24px; width: 24px;" class="icon malibu-icon fill-gray" >
                        <title id="malibu-icon-ember490">Organizations</title>
                        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#group-28"></use>
                    </svg>
                    <span class="sub-nav-item-name gray">Organizations</span>
                </a>
            </div>
        </div>
    </nav>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
    props: {
        isAccessTokenActive: {
            type: Boolean,
            default: false
        },
        isAccountSettingActive: {
            type: Boolean,
            default: false
        },
        isOrganizationsActive: {
            type: Boolean,
            default: false
        }
    },
    setup(props) {
        const router = useRouter()

        const goToAccessToken = () => {
            router.push('/access-tokens')
        }

        const goToAccountSetting = () => {
            router.push('/account-setting')
        }

        const goToOrganizations = () => {
            router.push('/organizations')
        }

        return {
            goToAccessToken,
            goToAccountSetting,
            goToOrganizations
        }
    }
}
</script>

<style scoped>
    a:hover {
        cursor: pointer;
    }
</style>
