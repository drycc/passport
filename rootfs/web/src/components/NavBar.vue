<!--导航栏-->
<template>
  <nav class="glostick">
    <div class="glostick__property">
      <a class="glostick__property__name" href="/">
        <el-icon size="2.5rem" class="icon-logo">
          <img src="../../src/assets/icons/drycc.svg" />
        </el-icon>
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
