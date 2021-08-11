<!--用户菜单-->
<template>
    <a class="glostick__menu-icon glostick__menu-icon--account" @click="openOrCloseMenu">
        <div class="glostick__user__avatar--container">
            <img class="glostick__user__avatar" src="https://gravatar.com/avatar/02a485fa5edb11e2b5ca38e18622eacd?s=96&amp;d=/src/assets/style/ninja-avatar-96x96.png" id="menu-account">
        </div>
        <div class="glostick__user__notification "></div>
    </a>
    <ul id="glostick__menu--account" class="glostick__menu glostick__menu--account" :class="{'glostick__menu--open': isMenuActived}">
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--account-details" href="/account">
                <div class="glostick__user__avatar--container">
                    <img class="glostick__account-details__avatar" src="https://gravatar.com/avatar/02a485fa5edb11e2b5ca38e18622eacd?s=96&amp;d=/src/assets/style/ninja-avatar-96x96.png" >
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
            <a class="glostick__menu__item glostick__menu__item--settings" href="/account">Account settings</a>
        </li>

        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--docs" href="/expense-bills">Expense bills</a>
        </li>

        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--notifications" href="/notifications">Notifications</a>
        </li>
        <li :style="{display: isHiddenAdmin ? 'none': 'block' }" class="glostick__menu__listitem">
          <a :href="adminUrl" class="glostick__menu__item glostick__menu__item--signout" @click="admin">Admin</a>
        </li>
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--signout" @click="logout">Sign out</a>
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
