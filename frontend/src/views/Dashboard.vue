<template>
  <div class="dashboard-container">
    <el-card>
      <div class="nav-links">
        <el-link class="nav-link" @click="$router.push('/loan-records')">{{ $t('common.loanRecords') }}</el-link>
        <span style="margin: 0 10px; color: #dcdfe6;">|</span>
        <el-link class="nav-link" @click="$router.push('/vehicle-info')">{{ $t('common.vehicleInfo') }}</el-link>
        <span style="margin: 0 10px; color: #dcdfe6;">|</span>
        <el-link class="nav-link usage-link" @click="$router.push('/usage')">{{ $t('common.usageGuide') }}</el-link>
        <span style="margin: 0 10px; color: #dcdfe6;">|</span>
        <el-link class="nav-link" @click="$router.push('/admin')">{{ $t('common.admin') }}</el-link>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2 class="welcome-text">{{ $t('dashboard.welcome', { name: userName }) }}</h2>
        <div style="display: flex; align-items: center; gap: 15px;">
          <el-link v-if="isOTPAdmin" type="primary" class="nav-link" @click="$router.push('/otp-management')">{{ $t('common.otpManagement', 'OTP管理') }}</el-link>
          <el-button class="large-btn logout-btn" @click="handleLogout">{{ $t('common.logout') }}</el-button>
        </div>
      </div>

      <!-- Persistent Password Display -->
      <div v-if="activeOTP" class="password-display-container">
        <span class="password-label">
          {{ activeOTP.type === 'PICKUP' ? $t('dashboard.pickupCode') : $t('dashboard.returnCode') }}：
        </span>
        <span class="password-code">{{ activeOTP.code }}</span>
      </div>

      <!-- Return Assets Section -->
      <div v-if="heldAssets.length > 0" class="section-container" style="margin-top: 20px;">
        <h3 class="section-title">{{ $t('dashboard.return') }}</h3>
        <el-table :data="heldAssets" style="width: 100%" class="large-table">
          <el-table-column prop="identifier" :label="$t('dashboard.identifier')" />
          <el-table-column :label="$t('dashboard.type')">
            <template #default="scope">
              {{ $t('dashboard.assetTypes.' + scope.row.type) }}
            </template>
          </el-table-column>
        </el-table>
        <div style="margin-top: 20px; text-align: right;">
          <el-button type="danger" class="large-btn" :loading="loading" @click="handleReturn">{{ $t('dashboard.returnAction') }}</el-button>
        </div>
      </div>

      <!-- Pickup Assets Section (Inventory) -->
      <div class="section-container" :style="{ marginTop: heldAssets.length > 0 ? '40px' : '20px' }">
        <h3 class="section-title">{{ $t('dashboard.pickup') }}</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-table 
              :data="availableVehicles" 
              style="width: 100%" 
              @row-click="handleVehicleClick"
              :row-class-name="tableRowClassName"
              row-key="id"
              class="large-table"
            >
              <el-table-column prop="identifier" :label="$t('dashboard.assetTypes.KEY')" />
            </el-table>
          </el-col>
          <el-col :span="12">
            <el-table 
              :data="availableGasCards" 
              style="width: 100%" 
              @row-click="handleGasCardClick"
              :row-class-name="tableRowClassName"
              row-key="id"
              class="large-table"
            >
              <el-table-column prop="identifier" :label="$t('dashboard.assetTypes.GAS_CARD')" />
            </el-table>
          </el-col>
        </el-row>
        
        <div style="margin-top: 20px; text-align: right;">
          <el-button type="primary" class="large-btn" :disabled="selectedAssets.length === 0" :loading="loading" @click="handlePickup">{{ $t('dashboard.pickupSelected') }}</el-button>
        </div>
      </div>

      <!-- Loaned Items Section -->
      <div v-if="loanRecords.length > 0" class="section-container" style="margin-top: 40px;">
        <h3 class="section-title">{{ $t('dashboard.loan') }}</h3>
        <LoanList :loans="loanRecords" class="large-table" />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import api from '../api/client'
import LoanList from '../components/LoanList.vue'
import type { Asset, PickupResponse, ReturnResponse, ActiveLoan } from '../types/api'

useI18n()
const router = useRouter()
const userId = localStorage.getItem('user_id')
const userName = localStorage.getItem('user_name') || ''
const assets = ref<Asset[]>([])
const loanRecords = ref<ActiveLoan[]>([])
const loading = ref(false)

const isOTPAdmin = computed(() => {
  return localStorage.getItem('user_name') === import.meta.env.VITE_OTP_ADMIN_NAME
})

const selectedVehicle = ref<Asset | null>(null)
const selectedGasCard = ref<Asset | null>(null)

interface ActiveOTP {
  code: string;
  type: 'PICKUP' | 'RETURN';
  expires_at: string;
}

const activeOTP = ref<ActiveOTP | null>(null)

watch(activeOTP, (newVal) => {
  if (newVal) {
    localStorage.setItem('active_otp', JSON.stringify(newVal))
  } else {
    localStorage.removeItem('active_otp')
  }
}, { deep: true })

const checkExpiration = () => {
  if (activeOTP.value) {
    const expiresAt = new Date(activeOTP.value.expires_at)
    if (expiresAt <= new Date()) {
      activeOTP.value = null
    }
  }
}

let expirationTimer: any = null

onMounted(() => {
  if (!userId) {
    router.push('/')
    return
  }
  fetchAssets()
  fetchLoans()
  
  const savedOTP = localStorage.getItem('active_otp')
  if (savedOTP) {
    activeOTP.value = JSON.parse(savedOTP)
    checkExpiration()
  }
  expirationTimer = setInterval(checkExpiration, 60000)
})

onUnmounted(() => {
  if (expirationTimer) clearInterval(expirationTimer)
})

const fetchAssets = async () => {
  try {
    const response = await api.get<Asset[]>('/assets')
    assets.value = response.data
    // Clear selection on refresh if assets no longer available
    if (selectedVehicle.value && !availableVehicles.value.find(v => v.id === selectedVehicle.value?.id)) {
      selectedVehicle.value = null
    }
    if (selectedGasCard.value && !availableGasCards.value.find(g => g.id === selectedGasCard.value?.id)) {
      selectedGasCard.value = null
    }
  } catch (error: any) {
    ElMessage.error(error)
  }
}

const fetchLoans = async () => {
  try {
    const response = await api.get<ActiveLoan[]>('/assets/loans')
    loanRecords.value = response.data
  } catch (error: any) {
    ElMessage.error(error)
  }
}

const availableVehicles = computed(() => assets.value.filter(a => a.status === 'AVAILABLE' && a.type === 'KEY'))
const availableGasCards = computed(() => assets.value.filter(a => a.status === 'AVAILABLE' && a.type === 'GAS_CARD'))
const heldAssets = computed(() => assets.value.filter(a => a.status === 'CHECKED_OUT' && a.current_holder_id === userId))

const selectedAssets = computed(() => {
  const result = []
  if (selectedVehicle.value) result.push(selectedVehicle.value)
  if (selectedGasCard.value) result.push(selectedGasCard.value)
  return result
})

const handleVehicleClick = (row: Asset) => {
  if (selectedVehicle.value?.id === row.id) {
    selectedVehicle.value = null
  } else {
    selectedVehicle.value = row
  }
}

const handleGasCardClick = (row: Asset) => {
  if (selectedGasCard.value?.id === row.id) {
    selectedGasCard.value = null
  } else {
    selectedGasCard.value = row
  }
}

const tableRowClassName = ({ row }: { row: Asset }) => {
  if (selectedVehicle.value?.id === row.id || selectedGasCard.value?.id === row.id) {
    return 'selected-row'
  }
  return ''
}

const handlePickup = async () => {
  loading.value = true
  try {
    const assetIds = selectedAssets.value.map(a => a.id)
    const response = await api.post<PickupResponse>('/pickup', {
      user_id: userId,
      asset_ids: assetIds
    })
    
    activeOTP.value = {
      code: response.data.otp,
      type: 'PICKUP',
      expires_at: response.data.expires_at
    }
    
    selectedVehicle.value = null
    selectedGasCard.value = null
    fetchAssets()
    fetchLoans()
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

const handleReturn = async () => {
  loading.value = true
  try {
    const assetIds = heldAssets.value.map(a => a.id)
    const response = await api.post<ReturnResponse>('/return', {
      user_id: userId,
      asset_ids: assetIds
    })
    
    activeOTP.value = {
      code: response.data.otp,
      type: 'RETURN',
      expires_at: response.data.expires_at
    }
    
    fetchAssets()
    fetchLoans()
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
  activeOTP.value = null
  localStorage.removeItem('user_id')
  localStorage.removeItem('user_name')
  router.push('/')
}
</script>

<style scoped>
.nav-link {
  font-size: 20px;
}

.welcome-text {
  font-size: 28px;
}

.section-title {
  font-size: 24px;
  font-weight: bold;
}

.large-btn {
  font-size: 20px;
  padding: 12px 24px;
  height: auto;
}

.logout-btn {
  border: 2px solid #00008b !important;
  color: #00008b !important;
}

.large-table :deep(.el-table__header),
.large-table :deep(.el-table__body) {
  font-size: 18px;
}

.usage-link {
  color: #6ec6ff;
}

.usage-link:hover {
  color: #4fb5f2;
}

.nav-links {
  text-align: center;
  margin-bottom: 20px;
}
</style>

<style scoped>
.password-display-container {
  margin: 20px 0;
  padding: 15px;
  border: 2px solid #67C23A;
  border-radius: 4px;
  background-color: #f0f9eb;
  text-align: center;
}

.password-label {
  font-size: 22px;
  font-weight: bold;
  color: #303133;
}

.password-code {
  font-size: 32px;
  font-weight: bold;
  color: #67C23A;
  margin-left: 10px;
}

:deep(.selected-row td.el-table__cell) {
  background-color: lightgreen !important;
}

:deep(.el-table .selected-row:hover td.el-table__cell) {
  background-color: lightgreen !important;
}

@media (max-width: 768px) {
  .dashboard-container {
    font-size: 25px;
  }

  .nav-links {
    font-size: 25px;
  }

  :deep(.el-table) {
    font-size: 25px;
  }
}
</style>
