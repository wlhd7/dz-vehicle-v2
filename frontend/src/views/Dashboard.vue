<template>
  <div class="dashboard-container">
    <el-card>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>{{ $t('dashboard.welcome', { name: userName }) }}</h2>
        <el-button @click="handleLogout">{{ $t('common.logout') }}</el-button>
      </div>

      <!-- Return Assets Section -->
      <div v-if="heldAssets.length > 0" class="section-container" style="margin-top: 20px;">
        <h3>{{ $t('dashboard.return') }}</h3>
        <el-table :data="heldAssets" style="width: 100%">
          <el-table-column prop="identifier" :label="$t('dashboard.identifier')" />
          <el-table-column :label="$t('dashboard.type')">
            <template #default="scope">
              {{ $t('dashboard.assetTypes.' + scope.row.type) }}
            </template>
          </el-table-column>
        </el-table>
        <div style="margin-top: 20px; text-align: right;">
          <el-button type="danger" :loading="loading" @click="handleReturn">{{ $t('dashboard.returnAction') }}</el-button>
        </div>
      </div>

      <!-- Pickup Assets Section -->
      <div class="section-container" :style="{ marginTop: heldAssets.length > 0 ? '40px' : '20px' }">
        <h3>{{ $t('dashboard.pickup') }}</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-table 
              :data="availableVehicles" 
              style="width: 100%" 
              @row-click="handleVehicleClick"
              :row-class-name="tableRowClassName"
              row-key="id"
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
            >
              <el-table-column prop="identifier" :label="$t('dashboard.assetTypes.GAS_CARD')" />
            </el-table>
          </el-col>
        </el-row>
        
        <div style="margin-top: 20px; text-align: right;">
          <el-button type="primary" :disabled="selectedAssets.length === 0" :loading="loading" @click="handlePickup">{{ $t('dashboard.pickupSelected') }}</el-button>
        </div>
      </div>
    </el-card>
    
    <el-dialog v-model="otpDialogVisible" :title="$t('dashboard.otpTitle')" width="300">
      <div style="text-align: center;">
        <p>{{ $t('dashboard.otpSubtitle') }}</p>
        <h1 style="font-size: 48px; margin: 20px 0;">{{ otpCode }}</h1>
        <p style="color: #666;">{{ $t('dashboard.otpExpires', { time: formatDateTime(otpExpires) }) }}</p>
      </div>
      <template #footer>
        <el-button type="primary" @click="otpDialogVisible = false">{{ $t('dashboard.gotIt') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api/client'
import type { Asset, PickupResponse, ReturnResponse } from '../types/api'

const { t } = useI18n()
const router = useRouter()
const userId = localStorage.getItem('user_id')
const userName = localStorage.getItem('user_name') || 'User'
const assets = ref<Asset[]>([])
const loading = ref(false)

const selectedVehicle = ref<Asset | null>(null)
const selectedGasCard = ref<Asset | null>(null)

const otpDialogVisible = ref(false)
const otpCode = ref('')
const otpExpires = ref('')

onMounted(() => {
  if (!userId) {
    router.push('/')
    return
  }
  fetchAssets()
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

const formatDateTime = (dateStr: string) => {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    return new Intl.DateTimeFormat('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    }).format(date)
  } catch (e) {
    return dateStr
  }
}

const availableVehicles = computed(() => assets.value.filter(a => a.status === 'AVAILABLE' && a.type === 'KEY'))
const availableGasCards = computed(() => assets.value.filter(a => a.status === 'AVAILABLE' && a.type === 'GAS_CARD'))
const heldAssets = computed(() => assets.value.filter(a => a.status === 'CHECKED_OUT')) // In a real app, this should filter by user_id from backend

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
    
    otpCode.value = response.data.otp
    otpExpires.value = response.data.expires_at
    otpDialogVisible.value = true
    
    selectedVehicle.value = null
    selectedGasCard.value = null
    fetchAssets()
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
    
    ElMessageBox.alert(
      t('dashboard.returnCodeMessage', { otp: response.data.otp }), 
      t('dashboard.returnCodeTitle')
    )
    fetchAssets()
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
  localStorage.removeItem('user_id')
  localStorage.removeItem('user_name')
  router.push('/')
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

:deep(.selected-row) {
  background-color: #f0f9eb !important;
}
</style>
