<!--用户菜单-->
<template v-if="user.username != null">
    <dropdown
        trigger-id="menu-account"
        menu-id="ui-user-menu--account"
        trigger-label="Account"
        :trigger-icon="accountTriggerIcon"
        :items="menuItems"
        meta-label="Signed in as"
        :meta-value="user.email || user.username"
        :menu-width="226"
        :hide-label-on-mobile="true"
        @action="handleMenuAction"
    />
</template>

<script>
import { UserFilled } from "@element-plus/icons-vue"
import Dropdown from "./Dropdown.vue"
import UserMenu from "./UserMenu";

UserMenu.components = {
    ...(UserMenu.components || {}),
    Dropdown,
    UserFilled,
};

export default UserMenu;
</script>
