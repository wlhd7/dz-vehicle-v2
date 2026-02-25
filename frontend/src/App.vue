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
}

.full-page {
  width: 100vw;
}

.app-main {
  min-height: 100vh;
}
</style>
