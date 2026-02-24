<template>
  <div class="admin-container">
    <el-card>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>Admin Management</h2>
        <el-button @click="$router.push('/')">Go to Login</el-button>
      </div>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-card shadow="never" style="margin-top: 20px;">
            <h3>Add New Asset</h3>
            <el-form :model="assetForm" label-width="100px">
              <el-form-item label="Type">
                <el-select v-model="assetForm.type" placeholder="Select type">
                  <el-option label="KEY" value="KEY" />
                  <el-option label="GAS_CARD" value="GAS_CARD" />
                </el-select>
              </el-form-item>
              <el-form-item label="Identifier">
                <el-input v-model="assetForm.identifier" placeholder="Plate or Card Number" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleAddAsset" :loading="loading">Add Asset</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card shadow="never" style="margin-top: 20px;">
            <h3>Whitelist New User</h3>
            <el-form :model="userForm" label-width="100px">
              <el-form-item label="Full Name">
                <el-input v-model="userForm.name" placeholder="Alice Smith" />
              </el-form-item>
              <el-form-item label="ID Last 4">
                <el-input v-model="userForm.id_last4" placeholder="5678" maxlength="4" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleAddUser" :loading="loading">Add User</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>

      <el-card shadow="never" style="margin-top: 20px;">
        <h3>OTP Pool Management</h3>
        <div style="display: flex; align-items: center; gap: 20px;">
          <span>Current pool count: {{ otpCount }}</span>
          <el-input-number v-model="seedCount" :min="10" :max="500" />
          <el-button type="warning" @click="handleSeedOTPs" :loading="loading">Seed New OTPs</el-button>
        </div>
      </el-card>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api/client'

const loading = ref(false)
const otpCount = ref(0)
const seedCount = ref(100)

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
    ElMessage.success('Asset added successfully')
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
    ElMessage.success('User whitelisted successfully')
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
    ElMessage.success(`Added ${response.data.added} OTPs to pool`)
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
