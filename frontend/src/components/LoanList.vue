<template>
  <div class="loan-list">
    <el-table :data="loans" style="width: 100%">
      <el-table-column prop="identifier" :label="$t('dashboard.identifier')" />
      <el-table-column :label="$t('dashboard.type')">
        <template #default="scope">
          {{ $t('dashboard.assetTypes.' + scope.row.type) }}
        </template>
      </el-table-column>
      <el-table-column prop="user" :label="$t('dashboard.user')" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import type { ActiveLoan } from '../types/api'

defineProps<{
  loans: ActiveLoan[]
}>()
</script>

<style scoped>
.loan-list {
  margin-top: 10px;
}
</style>
