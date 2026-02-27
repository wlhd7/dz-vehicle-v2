<template>
  <div class="otp-management-container">
    <el-card>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>{{ $t('common.otpManagement', 'OTP管理') }}</h2>
        <el-button @click="goBack">{{ $t('common.back', '返回') }}</el-button>
      </div>
      
      <div style="margin-top: 30px;">
        <el-card shadow="never" class="info-card">
          <div class="count-display">
            <span class="label">剩余可用 OTP:</span>
            <span class="value">{{ loadingCount ? '...' : otpCount }}</span>
          </div>
        </el-card>
      </div>

      <div style="margin-top: 20px;">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="never">
              <h3>添加单笔 OTP</h3>
              <el-form :model="singleForm" label-width="80px" style="margin-top: 20px;" @submit.prevent="handleAddSingle">
                <el-form-item label="8位密码">
                  <el-input 
                    v-model="singleForm.password" 
                    placeholder="请输入8位数字密码" 
                    maxlength="8"
                    style="width: 200px; margin-right: 15px;"
                  />
                  <el-button type="primary" native-type="submit" :loading="addingSingle">添加</el-button>
                </el-form-item>
              </el-form>
            </el-card>
          </el-col>
          
          <el-col :span="12">
            <el-card shadow="never">
              <h3>批量导入 OTP</h3>
              <div style="margin-top: 20px;">
                <el-upload
                  action="#"
                  :auto-upload="false"
                  :show-file-list="true"
                  :on-change="handleFileChange"
                  :on-remove="handleFileRemove"
                  accept=".txt,.csv"
                  :limit="1"
                >
                  <template #trigger>
                    <el-button type="primary">选择文件</el-button>
                  </template>
                  <el-button 
                    style="margin-left: 10px;" 
                    type="success" 
                    @click="submitUpload"
                    :loading="uploading"
                    :disabled="!selectedFile"
                  >
                    上传到服务器
                  </el-button>
                  <template #tip>
                    <div class="el-upload__tip">
                      支持 .txt 或 .csv 文件，每个密码 8 位，以换行或逗号分隔
                    </div>
                  </template>
                </el-upload>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { UploadFile, UploadFiles } from 'element-plus'
import { getOTPCount, addSingleOTP, uploadOTPBatch } from '../api/client'

const router = useRouter()
const otpCount = ref(0)
const loadingCount = ref(false)
const addingSingle = ref(false)
const uploading = ref(false)
const selectedFile = ref<File | null>(null)

const singleForm = reactive({
  password: ''
})

const goBack = () => {
  router.push('/dashboard')
}

const fetchOTPCount = async () => {
  loadingCount.value = true
  try {
    const response = await getOTPCount()
    otpCount.value = response.data.count
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    loadingCount.value = false
  }
}

const handleAddSingle = async () => {
  const pwd = singleForm.password
  if (!pwd || pwd.length !== 8 || !/^\d+$/.test(pwd)) {
    ElMessage.error('请输入有效的8位数字密码')
    return
  }
  
  addingSingle.value = true
  try {
    const response = await addSingleOTP(pwd)
    ElMessage.success(response.data.message)
    otpCount.value = response.data.total_pool
    singleForm.password = ''
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    addingSingle.value = false
  }
}

const handleFileChange = (uploadFile: UploadFile, uploadFiles: UploadFiles) => {
  if (uploadFile.raw) {
    selectedFile.value = uploadFile.raw
  }
}

const handleFileRemove = () => {
  selectedFile.value = null
}

const submitUpload = async () => {
  if (!selectedFile.value) return
  
  uploading.value = true
  try {
    const response = await uploadOTPBatch(selectedFile.value)
    ElMessage.success(`成功导入 ${response.data.added} 个 OTP，当前池总数为 ${response.data.total_pool}`)
    otpCount.value = response.data.total_pool
    // Note: We don't automatically clear the file list in the UI for simplicity, 
    // the user can see it succeeded.
  } catch (error: any) {
    ElMessage.error(error)
  } finally {
    uploading.value = false
  }
}

onMounted(() => {
  fetchOTPCount()
})
</script>

<style scoped>
.otp-management-container {
  padding: 20px;
}

.info-card {
  border: 1px solid #e6a23c;
  background-color: #fdf6ec;
}

.count-display {
  display: flex;
  align-items: center;
  gap: 15px;
}

.label {
  font-size: 18px;
  font-weight: bold;
  color: #e6a23c;
}

.value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}
</style>
