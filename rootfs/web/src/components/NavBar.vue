<!--导航栏-->
<template>
  <nav class="glostick">
    <div class="glostick__property">
      <a class="glostick__property__name" href="/">
        <i class="icon-logo"></i>
        <svg width="62" height="11" viewBox="0 0 62 11" xmlns="http://www.w3.org/2000/svg"><title>Drycc</title><path d="M0 9.802h2.6V5.915h3.198v3.887h2.6V.182h-2.6v3.575H2.6V.182H0v9.62zm11.374 0h7.085V7.709h-4.485V5.928h3.042V3.9h-3.042V2.34h4.264V.182h-6.864v9.62zm9.567 0h2.548V6.461h.715l1.859 3.341h2.756l-2.041-3.679c1.26-.429 1.898-1.3 1.898-2.808 0-2.314-1.508-3.133-3.978-3.133H20.94v9.62zm2.548-5.317V2.288h1.118c1.066 0 1.534.286 1.534 1.092s-.468 1.105-1.534 1.105h-1.118zm12.257 5.499c2.314 0 4.72-1.469 4.72-4.992C40.465 1.469 38.06 0 35.745 0c-2.327 0-4.732 1.469-4.732 4.992 0 3.523 2.405 4.992 4.732 4.992zm0-2.08c-1.365 0-2.132-1.144-2.132-2.912s.767-2.847 2.132-2.847c1.352 0 2.12 1.079 2.12 2.847s-.768 2.912-2.12 2.912zm7.24 1.898h2.6v-2.99l.741-.858 2.275 3.848h2.938l-3.523-5.824L51.254.182h-3.016l-2.652 3.484V.182h-2.6v9.62zm14.624.143c2.808 0 4.03-1.456 4.03-4.004V.182h-2.548v5.746c0 1.326-.416 1.924-1.456 1.924s-1.469-.598-1.469-1.924V.182h-2.6v5.759c0 2.548 1.235 4.004 4.043 4.004z" fill="%238460AA" fill-rule="evenodd"></path></svg>
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
