<!--用户菜单-->
<template>
    <a class="glostick__menu-icon glostick__menu-icon--account" @click="openOrCloseMenu">
        <div class="glostick__user__avatar--container">
            <img class="glostick__user__avatar" src="../../src/assets/style/ninja-avatar-96x96.png" id="menu-account">
        </div>
        <div class="glostick__user__notification "></div>
    </a>
    <ul id="glostick__menu--account" class="glostick__menu glostick__menu--account" :class="{'glostick__menu--open': isMenuActived}">
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--account-details" href="/account-setting">
                <div class="glostick__user__avatar--container">
                    <img class="glostick__account-details__avatar" src="../../src/assets/style/ninja-avatar-96x96.png" >
                </div>
                <div class="glostick__account-details__name">
                  {{user.username}}
                </div>
                <div class="glostick__account-details__email">
                  {{user.email}}
                </div>
            </a>
        </li>
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--settings" href="/account-setting">Account settings</a>
        </li>

        <li class="glostick__menu__listitem">
          <a class="glostick__menu__item glostick__menu__item--docs" href="/user/logout">Sign out</a>
        </li>
    </ul>
</template>

<script>
import UserMenu from "./UserMenu"
export default UserMenu
</script>

<style scoped>
    @import "../assets/home.css";
    .glostick__menu--account {
        top: 42px
    }
</style>
