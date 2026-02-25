<template>
  <div class="admin-container">
    <el-card>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>{{ $t('vehicleInfo.title') }}</h2>
        <el-button @click="goBack">{{ $t('common.back') }}</el-button>
      </div>

      <!-- Security Settings -->
      <el-card v-if="!isMobile" shadow="never" style="margin-top: 20px; border: 1px solid #e6a23c; background-color: #fdf6ec;">
        <div style="display: flex; align-items: center; gap: 15px;">
          <strong style="color: #e6a23c;">{{ $t('admin.secretLabel') }}</strong>
          <el-input 
            v-model="adminSecret" 
            type="password" 
            :placeholder="$t('admin.secretPlaceholder')" 
            show-password
            style="width: 300px"
          />
          <el-button type="warning" @click="saveSecret">{{ $t('admin.saveSecret') }}</el-button>
        </div>
      </el-card>

      <!-- Vehicle List -->
      <div style="margin-top: 20px;">
        <el-table :data="vehicles" :row-class-name="tableRowClassName" style="width: 100%">
          <el-table-column prop="identifier" :label="$t('dashboard.identifier')" />
          <el-table-column :label="$t('vehicleInfo.maintenanceDate')">
            <template #default="scope">
              {{ formatDate(scope.row.maintenance_date) }}
            </template>
          </el-table-column>
          <el-table-column prop="maintenance_mileage" :label="$t('vehicleInfo.maintenanceMileage')" />
          <el-table-column :label="$t('vehicleInfo.inspectionDate')">
            <template #default="scope">
              {{ formatDate(scope.row.inspection_date) }}
            </template>
          </el-table-column>
          <el-table-column :label="$t('vehicleInfo.insuranceDate')">
            <template #default="scope">
              {{ formatDate(scope.row.insurance_date) }}
            </template>
          </el-table-column>
          <el-table-column :label="$t('dashboard.action')" width="120">
            <template #default="scope">
              <el-button size="small" @click="handleEdit(scope.row)">
                {{ $t('common.edit') }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Edit Dialog -->
      <el-dialog v-model="editDialogVisible" :title="$t('vehicleInfo.edit')" width="500px">
        <el-form :model="editForm" label-width="120px" v-if="currentVehicle">
          <el-form-item :label="$t('dashboard.identifier')">
            <el-input v-model="currentVehicle.identifier" disabled />
          </el-form-item>
          <el-form-item :label="$t('vehicleInfo.maintenanceDate')">
            <el-date-picker v-model="editForm.maintenance_date" type="datetime" style="width: 100%" />
          </el-form-item>
          <el-form-item :label="$t('vehicleInfo.maintenanceMileage')">
            <el-input-number v-model="editForm.maintenance_mileage" :min="0" :step="1000" style="width: 100%" />
          </el-form-item>
          <el-form-item :label="$t('vehicleInfo.inspectionDate')">
            <el-date-picker v-model="editForm.inspection_date" type="datetime" style="width: 100%" />
          </el-form-item>
          <el-form-item :label="$t('vehicleInfo.insuranceDate')">
            <el-date-picker v-model="editForm.insurance_date" type="datetime" style="width: 100%" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="editDialogVisible = false">{{ $t('common.cancel') }}</el-button>
            <el-button type="primary" :loading="loading" @click="saveEdit">{{ $t('common.save') }}</el-button>
          </span>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import api from '../api/client'
import type { Asset } from '../types/api'
import useIsMobile from '../composables/useIsMobile'

const { t } = useI18n()
const router = useRouter()
const loading = ref(false)
const adminSecret = ref(localStorage.getItem('admin_secret') || '')
const isMobile = useIsMobile()

const goBack = () => {
  if (localStorage.getItem('user_id')) {
    router.push('/dashboard')
  } else {
    router.push('/')
  }
}

const vehicles = ref<Asset[]>([])
const editDialogVisible = ref(false)
const currentVehicle = ref<Asset | null>(null)
const editForm = reactive({
  maintenance_date: null as Date | string | null,
  maintenance_mileage: null as number | null,
  inspection_date: null as Date | string | null,
  insurance_date: null as Date | string | null
})

const saveSecret = () => {
  localStorage.setItem('admin_secret', adminSecret.value)
  ElMessage.success(t('common.success'))
  fetchVehicles()
}

const fetchVehicles = async () => {
  try {
    const response = await api.get<Asset[]>('/assets?type=KEY')
    vehicles.value = response.data
  } catch (error: any) {
    ElMessage.error(error || 'Failed to fetch vehicles')
  }
}

const formatDate = (dateStr: string | undefined | null) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString()
}

// Check for warnings: maintenance > 6 months, inspection/insurance < 30 days
const hasWarning = (asset: Asset) => {
  const now = new Date()
  
  if (asset.maintenance_date) {
    const mDate = new Date(asset.maintenance_date)
    const diffMonths = (now.getFullYear() - mDate.getFullYear()) * 12 + (now.getMonth() - mDate.getMonth())
    if (diffMonths >= 6) return true
  }
  
  if (asset.inspection_date) {
    const iDate = new Date(asset.inspection_date)
    const diffDays = (iDate.getTime() - now.getTime()) / (1000 * 3600 * 24)
    if (diffDays <= 30 && diffDays > -365) return true // warn if expiring soon
  }
  
  if (asset.insurance_date) {
    const insDate = new Date(asset.insurance_date)
    const diffDays = (insDate.getTime() - now.getTime()) / (1000 * 3600 * 24)
    if (diffDays <= 30 && diffDays > -365) return true
  }
  
  return false
}

const tableRowClassName = ({ row }: { row: Asset }) => {
  if (hasWarning(row)) {
    return 'warning-row'
  }
  return ''
}

const handleEdit = (asset: Asset) => {
  currentVehicle.value = asset
  editForm.maintenance_date = asset.maintenance_date ? new Date(asset.maintenance_date) : null
  editForm.maintenance_mileage = asset.maintenance_mileage || null
  editForm.inspection_date = asset.inspection_date ? new Date(asset.inspection_date) : null
  editForm.insurance_date = asset.insurance_date ? new Date(asset.insurance_date) : null
  editDialogVisible.value = true
}

const saveEdit = async () => {
  if (!currentVehicle.value) return
  if (!localStorage.getItem('admin_secret')) {
    ElMessage.error('Admin secret required')
    return
  }
  
  loading.value = true
  try {
    const payload = {
      maintenance_date: editForm.maintenance_date ? new Date(editForm.maintenance_date).toISOString() : null,
      maintenance_mileage: editForm.maintenance_mileage,
      inspection_date: editForm.inspection_date ? new Date(editForm.inspection_date).toISOString() : null,
      insurance_date: editForm.insurance_date ? new Date(editForm.insurance_date).toISOString() : null
    }
    
    await api.patch(`/admin/assets/${currentVehicle.value.id}`, payload)
    ElMessage.success(t('common.success'))
    editDialogVisible.value = false
    fetchVehicles()
  } catch (error: any) {
    ElMessage.error(error || 'Update failed')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchVehicles()
})
</script>

<style scoped>
:deep(.warning-row) {
  background-color: #fdf6ec !important;
}
:deep(.warning-row td:first-child::after) {
  content: " ⚠️";
  color: #e6a23c;
}
</style>
