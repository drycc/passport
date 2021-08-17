<template>
    <ul id="glostick__menu--navigator" class="glostick__menu glostick__menu--navigator" :class="{'glostick__menu--open': isMenuActived}">
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--databases" href="https://github.com/drycc/">Github</a>
        </li>
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--dataclips" href="https://www.drycc.com">Docs</a>
        </li>
    </ul>
</template>

<script>
import NavMenu from "./NavMenu"
export default NavMenu
</script>

<style scoped>
    @import "../assets/home.css";
    .glostick__menu--navigator {
        top: 42px
    }
</style>
