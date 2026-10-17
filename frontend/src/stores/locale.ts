import { defineStore } from 'pinia'
import { ref } from 'vue'

export type Locale = 'es' | 'en'

export const useLocaleStore = defineStore('locale', () => {
  const saved = (typeof window !== 'undefined' ? localStorage.getItem('dramaapp_locale') : null) as Locale | null
  const currentLocale = ref<Locale>(saved === 'en' ? 'en' : 'es')

  if (typeof document !== 'undefined') {
    document.documentElement.lang = currentLocale.value
  }

  function setLocale(newLocale: Locale) {
    currentLocale.value = newLocale
    if (typeof window !== 'undefined') {
      localStorage.setItem('dramaapp_locale', newLocale)
      document.documentElement.lang = newLocale
    }
  }

  function toggleLocale() {
    setLocale(currentLocale.value === 'es' ? 'en' : 'es')
  }

  return {
    currentLocale,
    setLocale,
    toggleLocale,
  }
})
