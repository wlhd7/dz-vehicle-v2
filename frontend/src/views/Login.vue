<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>{{ $t('login.title') }}</h2>
      <el-form :model="form" @submit.prevent="handleVerify">
        <el-form-item :label="$t('login.name')">
          <el-input v-model="form.name" :placeholder="$t('login.namePlaceholder')" />
        </el-form-item>
        <el-form-item :label="$t('login.idDigits')">
          <el-input v-model="form.id_digits" :placeholder="$t('login.idDigitsPlaceholder')" maxlength="4" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleVerify" :loading="loading" block>{{ $t('login.submit') }}</el-button>
        </el-form-item>
      </el-form>
      <div style="margin-top: 20px; text-align: center;">
        <el-link @click="$router.push('/admin')">{{ $t('common.admin') }}</el-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import api from '../api/client'
import type { VerifyResponse } from '../types/api'

const { t } = useI18n()
const router = useRouter()
const loading = ref(false)
const form = reactive({
  name: '',
  id_digits: ''
})

const handleVerify = async () => {
  if (!form.name || !form.id_digits) {
    ElMessage.error(t('login.missingFields'))
    return
  }
  
  loading.value = true
  try {
    const response = await api.post<VerifyResponse>('/verify', form)
    localStorage.setItem('user_id', response.data.user_id)
    localStorage.setItem('user_name', form.name)
    ElMessage.success(t('common.success'))
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
