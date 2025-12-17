<template>
    <nav class="ui-subnav">
        <div class="ui-subnav__inner">
            <button @click="goToAccessToken" class="ui-subnav__item" :class="{'is-active': isAccessTokenActive}" type="button">
                <span>Access Tokens</span>
            </button>
            <button @click="goToAccountSetting" class="ui-subnav__item" :class="{'is-active': isAccountSettingActive}" type="button">
                <span>Account Setting</span>
            </button>
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
    },
    setup(props) {
        const router = useRouter()

        const goToAccessToken = () => {
            router.push('/access-tokens')
        }

        const goToAccountSetting = () => {
            router.push('/account-setting')
        }

        return {
            goToAccessToken,
            goToAccountSetting
        }
    }
}
</script>

<style scoped>
.ui-subnav {
    padding: 14px 16px 8px;
    border-bottom: 1px solid rgba(217, 226, 239, 0.75);
    background: linear-gradient(180deg, rgba(247, 250, 255, 0.95) 0%, rgba(255, 255, 255, 1) 100%);
}

.ui-subnav__inner {
    display: flex;
    gap: 8px;
    padding: 0;
    flex-wrap: wrap;
}

.ui-subnav__item {
    border: none;
    background: #edf2fa;
    color: var(--ui-color-text-secondary);
    padding: 9px 16px;
    border-radius: 999px;
    cursor: pointer;
    font-weight: var(--ui-font-weight-semibold);
    transition: all 0.18s ease;
}

.ui-subnav__item:hover {
    color: var(--ui-color-primary-hover);
    background: var(--ui-color-primary-soft);
}

.ui-subnav__item.is-active {
    color: #fff;
    background: var(--ui-color-primary);
    box-shadow: 0 8px 20px rgba(64, 158, 255, 0.34);
}
</style>
