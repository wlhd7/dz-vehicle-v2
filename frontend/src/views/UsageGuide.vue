<template>
  <div class="guide-container">
    <el-card>
      <div class="guide-header">
        <h2>{{ $t('common.usageGuide') }}</h2>
        <el-button @click="goBack">{{ $t('common.back') }}</el-button>
      </div>

      <div class="guide-section">
        <h3>1. 登陆</h3>
        <ul>
          <li>1.1. 领取前需登陆</li>
          <li>1.2. 登陆用户名为真实姓名，密码为身份证后四位</li>
        </ul>
      </div>

      <div class="guide-section">
        <h3>2. 领取</h3>
        <ul>
          <li>
            2.1. 每次可领取：
            <ul>
              <li>一辆车</li>
              <li>一张加油卡</li>
              <li>一辆车及一张加油卡</li>
            </ul>
          </li>
        </ul>
      </div>

      <div class="guide-section">
        <h3>3. 归还</h3>
        <ul>
          <li>3.1. 如果领取了车和加油卡，需同时归还</li>
        </ul>
      </div>

      <div class="guide-section">
        <h3>4. 客服</h3>
        <ul>
          <li>4.1 微信：18665373915</li>
          <li>4.2 手机：19128704613</li>
        </ul>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  if (localStorage.getItem('user_id')) {
    router.push('/dashboard')
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
.guide-container {
  text-align: left;
}

.guide-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.guide-section {
  margin-top: 20px;
}

.guide-section h3 {
  margin: 0 0 8px;
}

.guide-section ul {
  margin: 0;
  padding-left: 18px;
  list-style-type: none;
}

.guide-section ul ul {
  margin-top: 6px;
  padding-left: 18px;
}

.guide-section li {
  margin-bottom: 6px;
}
</style>
