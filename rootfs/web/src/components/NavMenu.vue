<template>
    <ul id="menu-navigator" class="ui-nav-menu" :class="{'ui-nav-menu--open': isMenuActived}">
        <li class="ui-nav-menu__item">
            <a class="ui-nav-menu__link" href="/">
                <el-icon class="ui-nav-menu__icon" aria-hidden="true"><Grid /></el-icon>
                <span>Dashboard</span>
            </a>
        </li>
        <li class="ui-nav-menu__item ui-nav-menu__item--dropdown">
            <dropdown
                trigger-id="menu-nav"
                menu-id="ui-nav-menu-resources"
                trigger-label="Resources"
                :trigger-icon="resourcesTriggerIcon"
                :items="resourceItems"
                :menu-width="226"
            />
        </li>
    </ul>
</template>

<script>
import { Connection, Document, Grid } from "@element-plus/icons-vue"
import NavMenu from "./NavMenu"
import Dropdown from "./Dropdown.vue"

NavMenu.components = {
    ...(NavMenu.components || {}),
    Dropdown,
    Grid,
    Connection,
    Document,
}

export default NavMenu
</script>

<style scoped>
.ui-nav-menu {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.ui-nav-menu__item {
    position: relative;
}

.ui-nav-menu__link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
    color: #4e5e76;
    font-size: var(--ui-font-size-xl);
    font-weight: var(--ui-font-weight-semibold);
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 8px 10px;
    background: transparent;
    transition: all 0.16s ease;
}

.ui-nav-menu__icon {
    font-size: var(--ui-font-size-2xl);
    color: var(--ui-color-primary);
}

.ui-nav-menu__icon :deep(svg) {
    stroke-width: 2.4;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.ui-nav-menu__link:hover {
    color: #394e6b;
    background: #f5f8fd;
    border-color: #e1e9f5;
}

.ui-nav-menu__link:hover .ui-nav-menu__icon {
    color: var(--ui-color-primary);
}

@media (max-width: 900px) {
    .ui-nav-menu {
        gap: 4px;
    }

    .ui-nav-menu__link {
        padding: 6px;
        font-size: var(--ui-font-size-md);
    }

    .ui-nav-menu__icon {
        font-size: var(--ui-font-size-xl);
    }
}
</style>
