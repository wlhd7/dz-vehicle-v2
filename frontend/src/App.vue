<template>
  <el-config-provider :locale="zhCn">
    <el-container class="app-container">
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-config-provider>
</template>

<script setup lang="ts">
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
</script>

<style>
.app-container {
  min-height: 100vh;
}
</style>
