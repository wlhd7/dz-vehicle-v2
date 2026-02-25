<template>
  <div class="login-container">
    <div class="login-card">
      <h2 style="text-align: center; margin-bottom: 30px;">{{ $t('login.title') }}</h2>
      <el-form :model="form" @submit.prevent="handleVerify" label-position="top" class="login-form">
        <el-form-item :label="$t('login.name')">
          <el-input v-model="form.name" :placeholder="$t('login.namePlaceholder')" />
        </el-form-item>
        <el-form-item :label="$t('login.idDigits')">
          <el-input v-model="form.id_digits" :placeholder="$t('login.idDigitsPlaceholder')" maxlength="4" />
        </el-form-item>
        <el-form-item class="button-item">
          <el-button type="primary" native-type="submit" :loading="loading" size="large" class="login-button">
            {{ $t('login.submit') }}
          </el-button>
        </el-form-item>
      </el-form>
      <div style="text-align: center;">
        <el-link @click="$router.push('/loan-records')">{{ $t('common.loanRecords') }}</el-link>
        <span style="margin: 0 10px; color: #dcdfe6;">|</span>
        <el-link @click="$router.push('/vehicle-info')">{{ $t('common.vehicleInfo') }}</el-link>
        <span style="margin: 0 10px; color: #dcdfe6;">|</span>
        <el-link class="usage-link" @click="$router.push('/usage')">{{ $t('common.usageGuide') }}</el-link>
        <span style="margin: 0 10px; color: #dcdfe6;">|</span>
        <el-link @click="$router.push('/admin')">{{ $t('common.admin') }}</el-link>
      </div>
    </div>
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
  width: 360px;
}
.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 40px;
}
:deep(.el-form-item) {
  width: 240px; /* Shortened and equal length */
  margin-bottom: 20px;
}
:deep(.el-form-item__label) {
  padding-bottom: 0px !important;
  text-align: left;
  font-weight: bold;
  font-size: 18px;
  width: 100%;
}
.login-button {
  width: 100%; /* Equal length to inputs */
  height: 44px; /* Enlarged button */
  font-size: 16px;
}
.button-item {
  margin-top: 25px;
}

.usage-link {
  color: #6ec6ff;
}

.usage-link:hover {
  color: #4fb5f2;
}
</style>
