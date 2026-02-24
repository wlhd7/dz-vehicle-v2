import { createI18n } from 'vue-i18n'
import zhCn from './locales/zh-cn.json'

const i18n = createI18n({
  legacy: false, // use Composition API
  locale: 'zh-cn',
  fallbackLocale: 'zh-cn',
  messages: {
    'zh-cn': zhCn
  }
})

export default i18n
