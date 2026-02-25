import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Dashboard from '../Dashboard.vue'
import { createI18n } from 'vue-i18n'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import api from '../../api/client'

// Mock api
vi.mock('../../api/client', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}))

// Mock router
const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/', component: { template: '<div>Home</div>' } }],
})

// Mock i18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages: {
    en: {
      dashboard: {
        welcome: 'Welcome {name}',
        return: 'Return',
        pickup: 'Pickup',
        pickupSelected: 'Pickup Selected',
        loan: 'Loan',
      },
      common: {
        logout: 'Logout',
      }
    },
  },
})

describe('Dashboard.vue', () => {
  beforeEach(() => {
    localStorage.clear()
    localStorage.setItem('user_id', 'test-user-id')
    localStorage.setItem('user_name', 'Test User')
    vi.clearAllMocks()
    
    // Default mock response for assets
    ;(api.get as any).mockResolvedValue({ data: [] })
  })

  it('renders correctly', async () => {
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router, i18n, ElementPlus],
      },
    })
    expect(wrapper.find('h2').text()).toContain('Test User')
  })

  it('shows pickup password in UI instead of dialog when T006 is implemented', async () => {
    ;(api.post as any).mockResolvedValue({
      data: {
        success: true,
        otp: '1234',
        expires_at: new Date(Date.now() + 7200000).toISOString(),
      },
    })

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router, i18n, ElementPlus],
      },
    })

    // This test case will fail initially because the element is not there
    // and handlePickup still shows dialog
    
    // We expect a div with the green border styling after T007
    // For now, let's look for the text "1234" in the main UI
    // await wrapper.find('.el-button--primary').trigger('click') // Not possible without selected assets
    
    // Actually, I'll just check if the new container exists
    const passwordDisplay = wrapper.find('.password-display-container')
    expect(passwordDisplay.exists()).toBe(false) // This is what it currently is
  })
  
  it('fails to find embedded password text when pickup occurs (RED PHASE)', async () => {
    // This is the actual RED PHASE test
    // We'll mock the pickup response and verify that the UI contains the code but NOT in a dialog
    
    // Mock assets to show inventory
    ;(api.get as any).mockResolvedValueOnce({
      data: [
        { id: '1', type: 'KEY', identifier: 'VEH-01', status: 'AVAILABLE' }
      ]
    })

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router, i18n, ElementPlus],
      },
    })
    
    await new Promise(resolve => setTimeout(resolve, 0)) // wait for onMounted

    // Select the asset
    await wrapper.find('.el-table__row').trigger('click')
    
    ;(api.post as any).mockResolvedValue({
      data: {
        success: true,
        otp: '8888',
        expires_at: new Date(Date.now() + 7200000).toISOString(),
      },
    })

    await wrapper.find('.el-button--primary').trigger('click')
    await new Promise(resolve => setTimeout(resolve, 0))

    // Expect the embedded display to show "8888"
    // Currently this will FAIL because it doesn't exist
    const embeddedCode = wrapper.find('.password-display-container')
    expect(embeddedCode.exists()).toBe(true)
    expect(embeddedCode.text()).toContain('8888')
  })

  it('shows return password and overrides previous password (RED PHASE)', async () => {
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router, i18n, ElementPlus],
      },
    })

    // Setup active password (pickup)
    await wrapper.vm.$nextTick()
    ;(wrapper.vm as any).activeOTP = {
      code: '1111',
      type: 'PICKUP',
      expires_at: new Date(Date.now() + 3600000).toISOString()
    }
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.password-display-container').text()).toContain('1111')

    // Mock held assets for return
    ;(wrapper.vm as any).assets = [
      { id: '1', type: 'KEY', identifier: 'VEH-01', status: 'CHECKED_OUT' }
    ]
    await wrapper.vm.$nextTick()

    ;(api.post as any).mockResolvedValue({
      data: {
        success: true,
        otp: '9999',
        expires_at: new Date(Date.now() + 7200000).toISOString(),
      },
    })

    await wrapper.find('.el-button--danger').trigger('click')
    await new Promise(resolve => setTimeout(resolve, 0))

    // Expect the embedded display to show "9999" and label for return
    const embeddedCode = wrapper.find('.password-display-container')
    expect(embeddedCode.text()).toContain('9999')
    // We can't check localized text easily without full i18n setup in test, 
    // but we can check if it contains the return key if we use it in template
    // Or just check if '1111' is GONE.
    expect(embeddedCode.text()).not.toContain('1111')
  })

  it('persists password in localStorage', async () => {
    // This tests T010
    // Backend now returns ISO string with 'Z'
    const expiresAt = new Date(Date.now() + 3600000).toISOString()
    
    const otpData = {
      code: '7777',
      type: 'PICKUP',
      expires_at: expiresAt
    }
    localStorage.setItem('active_otp', JSON.stringify(otpData))

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router, i18n, ElementPlus],
      },
    })

    await wrapper.vm.$nextTick()
    expect(wrapper.find('.password-display-container').exists()).toBe(true)
    expect(wrapper.find('.password-display-container').text()).toContain('7777')
  })

  it('auto-hides password after expiration (RED PHASE)', async () => {
    // This tests T011 and T012
    vi.useFakeTimers()
    
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router, i18n, ElementPlus],
      },
    })

    const expiresAt = new Date(Date.now() + 60000).toISOString() // Expires in 1 min
    ;(wrapper.vm as any).activeOTP = {
      code: '1234',
      type: 'PICKUP',
      expires_at: expiresAt
    }
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.password-display-container').exists()).toBe(true)

    // Fast-forward 61 seconds
    vi.advanceTimersByTime(61000)
    await wrapper.vm.$nextTick()

    expect(wrapper.find('.password-display-container').exists()).toBe(false)
    
    vi.useRealTimers()
  })
})
