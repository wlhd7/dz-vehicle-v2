<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>Vehicle Asset Pickup</h2>
      <el-form :model="form" @submit.prevent="handleVerify">
        <el-form-item label="Full Name">
          <el-input v-model="form.name" placeholder="John Doe" />
        </el-form-item>
        <el-form-item label="ID Last 4 Digits">
          <el-input v-model="form.id_digits" placeholder="1234" maxlength="4" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleVerify" :loading="loading" block>Verify Identity</el-button>
        </el-form-item>
      </el-form>
      <div style="margin-top: 20px; text-align: center;">
        <el-link @click="$router.push('/admin')">Admin Panel</el-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api/client'
import type { VerifyResponse } from '../types/api'

const router = useRouter()
const loading = ref(false)
const form = reactive({
  name: '',
  id_digits: ''
})

const handleVerify = async () => {
  if (!form.name || !form.id_digits) {
    ElMessage.error('Please enter both name and ID digits')
    return
  }
  
  loading.value = true
  try {
    const response = await api.post<VerifyResponse>('/verify', form)
    localStorage.setItem('user_id', response.data.user_id)
    localStorage.setItem('user_name', form.name)
    ElMessage.success('Verified successfully')
    router.push('/dashboard')
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}
.login-card {
  width: 400px;
}
</style>
