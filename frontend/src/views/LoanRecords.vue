<template>
  <div class="loan-records-container">
    <el-card>
      <div class="header">
        <h2>{{ $t('loanRecords.title') }}</h2>
        <el-button @click="goBack">{{ $t('common.back') }}</el-button>
      </div>

      <el-table 
        ref="tableRef"
        :data="paginatedRecords" 
        style="width: 100%" 
        v-loading="loading"
        @filter-change="handleFilterChange"
        @header-click="handleHeaderClick"
      >
        <el-table-column 
          prop="identifier" 
          :label="$t('loanRecords.identifier')"
          column-key="identifier"
          :filters="identifierFilters"
          :filter-multiple="false"
          header-class-name="filter-header"
        />
        <el-table-column 
          prop="type"
          :label="$t('loanRecords.type')"
          column-key="type"
          :filters="typeFilters"
          :filter-multiple="false"
          header-class-name="filter-header"
        >
          <template #default="scope">
            {{ $t('dashboard.assetTypes.' + scope.row.type) }}
          </template>
        </el-table-column>
        <el-table-column prop="user_name" :label="$t('loanRecords.user')" />
        <el-table-column :label="$t('loanRecords.loanTime')">
          <template #default="scope">
            {{ formatDate(scope.row.loan_time) }}
          </template>
        </el-table-column>
        <el-table-column :label="$t('loanRecords.returnTime')">
          <template #default="scope">
            {{ formatDate(scope.row.return_time) }}
          </template>
        </el-table-column>
        <template #empty>
          <el-empty :description="$t('common.noRecords')" />
        </template>
      </el-table>

      <div class="pagination-container" v-if="filteredRecords.length > pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          layout="prev, pager, next"
          :total="filteredRecords.length"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { getLoanRecords, getIdentifiers } from '../api/client'
import type { LoanHistoryRecord } from '../types/api'

const { t } = useI18n()
const router = useRouter()
const loading = ref(false)
const records = ref<LoanHistoryRecord[]>([])
const allIdentifiers = ref<string[]>([])
const currentPage = ref(1)
const pageSize = ref(8)

const goBack = () => {
  if (localStorage.getItem('user_id')) {
    router.push('/dashboard')
  } else {
    router.push('/')
  }
}

// Active filters
const activeFilters = ref<{ [key: string]: string[] }>({})

const fetchRecords = async () => {
  loading.value = true
  try {
    const [recordsRes, idsRes] = await Promise.all([
      getLoanRecords(),
      getIdentifiers()
    ])
    records.value = recordsRes.data
    allIdentifiers.value = idsRes.data
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRecords()
})

const typeFilters = computed(() => [
  { text: t('dashboard.assetTypes.KEY'), value: 'KEY' },
  { text: t('dashboard.assetTypes.GAS_CARD'), value: 'GAS_CARD' }
])

const identifierFilters = computed(() => {
  return allIdentifiers.value.map(id => ({ text: id, value: id }))
})

const handleFilterChange = (filters: any) => {
  activeFilters.value = { ...activeFilters.value, ...filters }
  currentPage.value = 1 // Reset to first page on filter change
}

const filteredRecords = computed(() => {
  return records.value.filter(record => {
    // Check type filter
    const typeFilter = activeFilters.value['type']
    if (typeFilter && typeFilter.length > 0 && !typeFilter.includes(record.type)) {
      return false
    }
    
    // Check identifier filter
    const idFilter = activeFilters.value['identifier']
    if (idFilter && idFilter.length > 0 && !idFilter.includes(record.identifier)) {
      return false
    }
    
    return true
  })
})

const paginatedRecords = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredRecords.value.slice(start, end)
})

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

const handleHeaderClick = (column: any, event: MouseEvent) => {
  if (column.columnKey === 'identifier' || column.columnKey === 'type') {
    // Find the filter trigger inside the clicked header
    const th = (event.target as HTMLElement).closest('th')
    if (th) {
      const trigger = th.querySelector('.el-table__column-filter-trigger') as HTMLElement
      if (trigger && !trigger.contains(event.target as Node)) {
        trigger.click()
      }
    }
  }
}

const formatDate = (dateStr: string | undefined | null) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  if (isNaN(date.getTime())) return ''
  
  const y = String(date.getFullYear()).slice(-2)
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const mm = String(date.getMinutes()).padStart(2, '0')
  
  return `${y}-${m}-${d} ${hh}:${mm}`
}
</script>

<style scoped>
.loan-records-container {
  max-width: 1000px;
  margin: 0 auto;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

:deep(.filter-header) {
  cursor: pointer;
}

:deep(.filter-header .cell) {
  display: flex;
  align-items: center;
}

:deep(.el-table__column-filter-trigger .el-icon) {
  color: #409eff; /* Primary blue to match UI */
  font-size: 14px;
}
</style>
