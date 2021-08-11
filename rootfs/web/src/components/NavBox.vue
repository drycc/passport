<!--子导航插槽组件-->
<template>
    <div class="top-nav flex flex-column justify-center">
        <div class="limit-width flex items-center flex-wrap">
            <div class="flex-auto f4">
                <nav class="crumb-trail flex items-center flex-auto f3 lh-copy near-black nudge-left--5 pv--3 ember-view">
                    <slot name="nav-cluster"></slot>
                </nav>
            </div>
            <slot name="create-new-app"></slot>
        </div>
        <div class="limit-width flex items-center flex-wrap"></div>
    </div>
</template>

<script>
import NavBox from "./NavBox"
export default NavBox
</script>

<style scoped>
    /*@import "../assets/bashboard.css";*/
</style>
