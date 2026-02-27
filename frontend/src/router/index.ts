import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Admin from '../views/Admin.vue'
import UsageGuide from '../views/UsageGuide.vue'
import VehicleInfo from '../views/VehicleInfo.vue'
import LoanRecords from '../views/LoanRecords.vue'
import OTPManagement from '../views/OTPManagement.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Login', component: Login },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard },
    { path: '/vehicle-info', name: 'VehicleInfo', component: VehicleInfo },
    { path: '/usage', name: 'UsageGuide', component: UsageGuide },
    { path: '/admin', name: 'Admin', component: Admin },
    { path: '/loan-records', name: 'LoanRecords', component: LoanRecords },
    { path: '/otp-management', name: 'OTPManagement', component: OTPManagement },
  ]
})

router.beforeEach((to, _, next) => {
  const userId = localStorage.getItem('user_id');

  if (to.path === '/' && userId) {
    next('/dashboard');
  } else if (to.path === '/dashboard' && !userId) {
    next('/');
  } else if (to.path === '/otp-management') {
    const isAdmin = localStorage.getItem('user_name') === import.meta.env.VITE_OTP_ADMIN_NAME;
    if (!isAdmin) {
      next('/dashboard');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router
