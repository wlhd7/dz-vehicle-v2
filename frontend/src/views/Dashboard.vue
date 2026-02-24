<template>
  <div class="dashboard-container">
    <el-card>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>Dashboard - Welcome, {{ userName }}</h2>
        <el-button @click="handleLogout">Logout</el-button>
      </div>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="Pickup Assets" name="pickup">
          <el-table :data="availableAssets" style="width: 100%" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" />
            <el-table-column prop="identifier" label="Identifier" />
            <el-table-column prop="type" label="Type" />
            <el-table-column prop="status" label="Status" />
          </el-table>
          
          <div style="margin-top: 20px; text-align: right;">
            <el-button type="primary" :disabled="selectedAssets.length === 0" :loading="loading" @click="handlePickup">Pickup Selected Assets</el-button>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="Return Assets" name="return">
           <el-table :data="heldAssets" style="width: 100%">
            <el-table-column prop="identifier" label="Identifier" />
            <el-table-column prop="type" label="Type" />
            <el-table-column label="Action">
              <template #default="scope">
                <el-button size="small" type="danger" @click="handleReturn(scope.row.id)" :loading="loading">Return</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    
    <el-dialog v-model="otpDialogVisible" title="Your Pickup Code" width="300">
      <div style="text-align: center;">
        <p>Use this code at the unattended terminal:</p>
        <h1 style="font-size: 48px; margin: 20px 0;">{{ otpCode }}</h1>
        <p style="color: #666;">Expires at: {{ otpExpires }}</p>
      </div>
      <template #footer>
        <el-button type="primary" @click="otpDialogVisible = false">Got it</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api/client'
import type { Asset, PickupResponse, ReturnResponse } from '../types/api'

const router = useRouter()
const userId = localStorage.getItem('user_id')
const userName = localStorage.getItem('user_name') || 'User'
const assets = ref<Asset[]>([])
const loading = ref(false)
const activeTab = ref('pickup')
const selectedAssets = ref<Asset[]>([])

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
  } catch (error: any) {
    ElMessage.error(error)
  }
}

const availableAssets = computed(() => assets.value.filter(a => a.status === 'AVAILABLE'))
const heldAssets = computed(() => assets.value.filter(a => a.status === 'CHECKED_OUT')) // In a real app, this should filter by user_id from backend

const handleSelectionChange = (val: Asset[]) => {
  selectedAssets.value = val
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
    
    fetchAssets()
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

const handleReturn = async (assetId: string) => {
  loading.value = true
  try {
    const response = await api.post<ReturnResponse>('/return', {
      user_id: userId,
      asset_id: assetId
    })
    
    ElMessageBox.alert(`Your return code is: ${response.data.otp}`, 'Return Code')
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
</style>
