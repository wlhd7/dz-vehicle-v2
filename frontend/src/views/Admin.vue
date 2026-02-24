<template>
  <div class="admin-container">
    <el-card>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>{{ $t('admin.title') }}</h2>
        <el-button @click="$router.push('/')">{{ $t('common.back') }}</el-button>
      </div>

      <!-- Security Settings -->
      <el-card shadow="never" style="margin-top: 20px; border: 1px solid #e6a23c; background-color: #fdf6ec;">
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
          <span style="font-size: 12px; color: #909399;">{{ $t('admin.secretNote') }}</span>
        </div>
      </el-card>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-card shadow="never" style="margin-top: 20px;">
            <h3>{{ $t('admin.addAsset') }}</h3>
            <el-form :model="assetForm" label-width="100px">
              <el-form-item :label="$t('admin.type')">
                <el-select v-model="assetForm.type" placeholder="">
                  <el-option label="KEY" value="KEY" />
                  <el-option label="GAS_CARD" value="GAS_CARD" />
                </el-select>
              </el-form-item>
              <el-form-item :label="$t('admin.identifier')">
                <el-input v-model="assetForm.identifier" :placeholder="$t('admin.identifierPlaceholder')" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleAddAsset" :loading="loading">{{ $t('admin.submitAsset') }}</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card shadow="never" style="margin-top: 20px;">
            <h3>{{ $t('admin.whitelistUser') }}</h3>
            <el-form :model="userForm" label-width="100px">
              <el-form-item :label="$t('login.name')">
                <el-input v-model="userForm.name" :placeholder="$t('login.namePlaceholder')" />
              </el-form-item>
              <el-form-item :label="$t('admin.idLast4')">
                <el-input v-model="userForm.id_last4" :placeholder="$t('admin.idLast4Placeholder')" maxlength="4" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleAddUser" :loading="loading">{{ $t('admin.submitUser') }}</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>

      <el-card shadow="never" style="margin-top: 20px;">
        <h3>{{ $t('admin.otpPool') }}</h3>
        <div style="display: flex; align-items: center; gap: 20px;">
          <span>{{ $t('admin.currentPool', { count: otpCount }) }}</span>
          <el-input-number v-model="seedCount" :min="10" :max="500" />
          <el-button type="warning" @click="handleSeedOTPs" :loading="loading">{{ $t('admin.seedOTPs') }}</el-button>
        </div>
      </el-card>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import api from '../api/client'

const { t } = useI18n()
const loading = ref(false)
const otpCount = ref(0)
const seedCount = ref(100)
const adminSecret = ref(localStorage.getItem('admin_secret') || '')

const saveSecret = () => {
  localStorage.setItem('admin_secret', adminSecret.value)
  ElMessage.success(t('common.success'))
}

const assetForm = reactive({
  type: 'KEY',
  identifier: ''
})

const userForm = reactive({
  name: '',
  id_last4: ''
})

const handleAddAsset = async () => {
  if (!assetForm.identifier) return
  loading.value = true
  try {
    await api.post('/admin/assets', assetForm)
    ElMessage.success(t('admin.assetAdded'))
    assetForm.identifier = ''
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

const handleAddUser = async () => {
  if (!userForm.name || !userForm.id_last4) return
  loading.value = true
  try {
    await api.post('/admin/users', userForm)
    ElMessage.success(t('admin.userWhitelisted'))
    userForm.name = ''
    userForm.id_last4 = ''
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

const handleSeedOTPs = async () => {
  loading.value = true
  try {
    const response = await api.post('/admin/seed-otps', { count: seedCount.value })
    otpCount.value = response.data.total_pool
    ElMessage.success(t('admin.otpsAdded', { added: response.data.added }))
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-container {
  padding: 20px;
}
</style>
