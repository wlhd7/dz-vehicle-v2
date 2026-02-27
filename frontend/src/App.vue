<template>
  <el-config-provider :locale="zhCn">
    <template v-if="isMobile">
      <div class="app-container full-page">
        <main class="app-main">
          <router-view />
        </main>
      </div>
    </template>
    <template v-else>
      <el-container class="app-container">
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </template>
  </el-config-provider>
</template>

<script setup lang="ts">
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import useIsMobile from './composables/useIsMobile'

const isMobile = useIsMobile()
</script>

<style>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.full-page {
  width: 100vw;
  height: 100vh;
}

.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Global overrides for mobile full-height experience */
@media (max-width: 768px) {
  /* Make the root div of any view flexible */
  .app-main > div {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .el-card {
    flex: 1;
    display: flex;
    flex-direction: column;
    border: none !important;
    border-radius: 0 !important;
  }

  .el-card__body {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 15px !important;
    overflow-y: auto;
  }
}
</style>
