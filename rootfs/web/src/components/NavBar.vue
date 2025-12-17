<!--导航栏-->
<template>
  <header class="ui-top-area">
    <nav class="ui-topbar">
      <div class="ui-topbar__layer">
        <div class="ui-topbar__brand-wrap">
          <a class="ui-topbar__brand" href="/">
            <el-icon size="2rem" class="ui-topbar__logo">
              <img src="../../src/assets/icons/drycc.svg" />
            </el-icon>
          </a>
        </div>
        <div class="ui-topbar__right">
          <div class="ui-topbar__center">
            <nav-menu />
          </div>
          <div class="ui-topbar__actions">
            <user-menu :user="user" />
          </div>
        </div>
      </div>
    </nav>
  </header>

</template>

<script>
import NavBar from "./NavBar"
export default NavBar
</script>

<style scoped>
.ui-top-area {
  position: sticky;
  top: 0;
  z-index: 40;
}

.ui-topbar {
  height: 68px;
  background: rgba(255, 255, 255, 0.95);
  border-bottom: 1px solid rgba(217, 226, 239, 0.88);
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 14px rgba(16, 42, 72, 0.06);
}

.ui-topbar__layer {
  width: min(var(--ui-shell-max-width), calc(100% - (var(--ui-shell-gutter) * 2)));
  max-width: none;
  margin: 0 auto;
  height: 100%;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
}

.ui-topbar__brand {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: auto;
  height: auto;
  padding: 0;
  border: none;
  background: transparent;
  text-decoration: none;
  line-height: 0;
}

.ui-topbar__brand-wrap {
  flex: 0 0 auto;
}

.ui-topbar__right {
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.ui-topbar__center {
  display: inline-flex;
  align-items: center;
}

.ui-topbar__actions {
  display: flex;
  align-items: center;
}

.ui-topbar__logo img {
  width: 40px;
  height: 40px;
  display: block;
}

@media (max-width: 900px) {
  .ui-topbar__layer {
    gap: 8px;
  }

  .ui-topbar {
    height: 60px;
  }

  .ui-topbar__center {
    justify-self: end;
  }

  .ui-topbar__right {
    gap: 0;
  }
}
</style>
