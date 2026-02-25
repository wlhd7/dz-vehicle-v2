import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Admin from '../views/Admin.vue'
import UsageGuide from '../views/UsageGuide.vue'
import VehicleInfo from '../views/VehicleInfo.vue'
import LoanRecords from '../views/LoanRecords.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Login', component: Login },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard },
    { path: '/vehicle-info', name: 'VehicleInfo', component: VehicleInfo },
    { path: '/usage', name: 'UsageGuide', component: UsageGuide },
    { path: '/admin', name: 'Admin', component: Admin },
    { path: '/loan-records', name: 'LoanRecords', component: LoanRecords },
  ]
})

export default router
