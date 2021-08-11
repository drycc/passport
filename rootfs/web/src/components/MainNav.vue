<template>
    <nav class="app-nav nav nav-tabs sub-nav ember-view">
        <div class="limit-width">
            <div class="sub-nav-item ember-view">
                <a @click="goToAppDetail" class="ember-view" :class="{'active': isOverviewActive}">
                    <svg style="height: 24px; width: 24px;"  class="icon malibu-icon fill-purple" >
                        <title id="malibu-icon-ember486">Overview</title>
                        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#overview-28"></use>
                    </svg>
                    <span class="sub-nav-item-name gray">Overview</span>
                </a>
            </div>
            <div class="sub-nav-item ember-view">
                <a @click="goToResources" class="ember-view" :class="{'active': isResourcesActive}">
                    <svg style="height: 24px; width: 24px;" class="icon malibu-icon fill-gray" >
                        <title id="malibu-icon-ember489">Resources</title>
                        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#formation-28"></use>
                    </svg>
                    <span class="sub-nav-item-name gray">Resources</span>
                </a>
            </div>

            <div class="sub-nav-item ember-view">
                <a @click="goToDeploy" class="ember-view" :class="{'active': isDeployActive}">
                    <svg style="height: 24px; width: 24px;" class="icon malibu-icon fill-gray" >
                        <title>Deploy</title>
                        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#deploy-28"></use>
                    </svg>
                    <span class="sub-nav-item-name gray">Deploy</span>
                </a>
            </div>

            <div class="sub-nav-item ember-view">
                <a @click="goToMetrics" class="ember-view" :class="{'active': isMetricsActive}">
                    <svg style="height: 24px; width: 24px;" class="icon malibu-icon fill-gray" >
                        <title id="malibu-icon-ember495">Metrics</title>
                        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#metrics-28"></use>
                    </svg>

                    <span class="sub-nav-item-name gray">Metrics</span>
                </a>
            </div>
            <div class="sub-nav-item ember-view">
                <a @click="goToActivity" class="ember-view" :class="{'active': isActivityActive}">
                    <svg style="height: 24px; width: 24px;"  class="icon malibu-icon fill-gray" >
                        <title >Activity</title>
                        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#time-28"></use>
                    </svg>

                    <span class="sub-nav-item-name gray">Activity</span>
                </a>
            </div>
            <div class="sub-nav-item ember-view">
                <a @click="goToAccess" class="ember-view" :class="{'active': isAccessActive}">
                    <svg style="height: 24px; width: 24px;" class="icon malibu-icon fill-gray" >
                        <title id="malibu-icon-ember501">Access</title>
                        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#team-28"></use>
                    </svg>
                    <span class="sub-nav-item-name gray">Access</span>
                </a>
            </div>

            <div class="sub-nav-item ember-view">
                <a @click="goToSettings" class="ember-view" :class="{'active': isSettingsActive}">
                    <svg style="height: 24px; width: 24px;"  class="icon malibu-icon fill-gray" >
                        <title id="malibu-icon-ember504">Settings</title>
                        <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#settings-28"></use>
                    </svg>

                    <span class="sub-nav-item-name gray">Settings</span>
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
