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
        </div>
    </nav>
</template>

<script>
import MainNav from "./MainNav"
export default MainNav
</script>

<style scoped>
    a:hover {
        cursor: pointer;
    }
</style>
