<!--导航栏-->
<template>
  <nav class="glostick">
    <div class="glostick__property">
      <a class="glostick__property__name" href="/">
        <icon-app-store size="3rem" class="icon-logo"/>
        <span>DRYCC</span>
      </a>
    </div>
    <div class="glostick__user">
      <nav-menu />
      <user-menu />
    </div>

  </nav>

</template>

<script>
import NavBar from "./NavBar"
export default NavBar
</script>

<style scoped>
  @import "../assets/home.css";
</style>
