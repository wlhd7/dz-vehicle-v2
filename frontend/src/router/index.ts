import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Admin from '../views/Admin.vue'
import VehicleInfo from '../views/VehicleInfo.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Login', component: Login },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard },
    { path: '/admin', name: 'Admin', component: Admin },
    { path: '/vehicle-info', name: 'VehicleInfo', component: VehicleInfo },
  ]
})

export default router
