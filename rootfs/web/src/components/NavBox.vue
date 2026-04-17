<!--子导航插槽组件-->
<template>
    <div class="ui-nav-box">
        <div class="ui-nav-box__inner">
            <div class="ui-nav-box__cluster">
                <nav class="ui-nav-box__trail">
                    <slot name="nav-cluster"></slot>
                </nav>
            </div>
            <slot name="create-new-app"></slot>
        </div>
        <div class="ui-nav-box__inner"></div>
    </div>
</template>

<script lang="ts">
export default {
    name: "NavBox"
}

</script>

<style scoped>
.ui-nav-box {
    padding: 8px 0;
}

.ui-nav-box__inner {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
}

.ui-nav-box__cluster {
    flex: 1;
}

.ui-nav-box__trail {
    display: flex;
    align-items: center;
    color: var(--ui-color-text);
    font-size: var(--ui-font-size-2xl);
    line-height: 1.4;
}
</style>
