import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '../types'
import { authService } from '../services/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('dramaapp_token'))
  const user = ref<User | null>(
    (() => {
      const saved = localStorage.getItem('dramaapp_user')
      if (saved) {
        try {
          return JSON.parse(saved) as User
        } catch {
          return null
        }
      }
      return null
    })()
  )
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(email: string, pass: string): Promise<boolean> {
    loading.value = true
    error.value = null
    try {
      const res = await authService.login(email, pass)
      token.value = res.token
      user.value = res.user
      return true
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al iniciar sesión'
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout(): Promise<void> {
    loading.value = true
    try {
      await authService.logout()
    } finally {
      token.value = null
      user.value = null
      loading.value = false
    }
  }

  async function initAuth(): Promise<void> {
    if (token.value) {
      try {
        const u = await authService.getCurrentUser()
        if (u) {
          user.value = u
        }
      } catch (err) {
        console.warn('initAuth revalidation error:', err)
      }
    }
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    login,
    logout,
    initAuth,
  }
})
