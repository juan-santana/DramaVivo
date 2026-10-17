<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { useToast } from '../../composables/useToast'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const toast = useToast()

const email = ref('')
const password = ref('')
const loading = ref(false)

function fillDemo() {
  email.value = 'admin'
  password.value = 'admin123'
}

async function handleLogin() {
  if (!email.value || !password.value) {
    toast.warning('Por favor ingresa usuario o correo y contraseña.')
    return
  }

  loading.value = true
  const success = await authStore.login(email.value, password.value)
  loading.value = false

  if (success) {
    toast.success('Bienvenido al panel maestro de DramaVivo.')
    const redirect = (route.query.redirect as string) || '/admin'
    router.push(redirect)
  } else {
    toast.error(authStore.error || 'Credenciales incorrectas.')
  }
}
</script>

<template>
  <div class="min-h-screen bg-background flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Ambient light glow -->
    <div class="absolute -top-32 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-32 -right-32 w-96 h-96 bg-secondary/15 rounded-full blur-3xl pointer-events-none"></div>

    <div class="w-full max-w-md glass-panel p-8 rounded-3xl border border-surface-border shadow-2xl relative z-10 space-y-6">
      <!-- Header with DramaVivo Branding -->
      <div class="text-center space-y-2">
        <router-link to="/" class="inline-flex items-center gap-3 mb-2 group">
          <!-- Custom Futuristic DramaVivo Emblem -->
          <div class="relative w-10 h-10 flex items-center justify-center">
            <div class="absolute inset-0 bg-gradient-to-tr from-rose-500 via-amber-400 to-purple-600 rounded-2xl blur-[6px] opacity-70 group-hover:opacity-100 transition-opacity"></div>
            <div class="relative w-10 h-10 rounded-2xl bg-[#12121a]/90 border border-white/20 p-2 flex items-center justify-center backdrop-blur-md group-hover:scale-105 transition-transform shadow-lg">
              <svg class="w-full h-full" viewBox="0 0 32 32" fill="none">
                <path d="M6 7L16 25L26 7" stroke="url(#dv-login-g1)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M11 7L16 16L21 7" stroke="url(#dv-login-g2)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
                <circle cx="16" cy="16" r="2.2" fill="#F5C518" />
                <defs>
                  <linearGradient id="dv-login-g1" x1="6" y1="7" x2="26" y2="25" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#FF2E55" />
                    <stop offset="0.5" stop-color="#FF9E00" />
                    <stop offset="1" stop-color="#9333EA" />
                  </linearGradient>
                  <linearGradient id="dv-login-g2" x1="11" y1="7" x2="21" y2="16" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#FFD700" />
                    <stop offset="1" stop-color="#FF2E55" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </div>

          <span class="text-2xl font-black text-white flex items-center">
            Drama<span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-rose-500 to-purple-400 ml-0.5">Vivo</span>
          </span>
        </router-link>
        <h2 class="text-xl font-bold text-white tracking-wide">Acceso Administrativo</h2>
        <p class="text-xs text-text-muted">Control de microdramas, analítica en vivo y gestión de derechos</p>
      </div>

      <!-- Demo Shortcut Pill -->
      <div class="p-3 rounded-xl bg-surface border border-surface-border flex items-center justify-between text-xs">
        <div>
          <span class="font-bold text-white block">Credenciales de Acceso</span>
          <span class="text-[11px] text-text-muted">admin / admin123</span>
        </div>
        <button
          type="button"
          @click="fillDemo"
          class="px-2.5 py-1 rounded-lg bg-surface-lighter hover:bg-surface-light text-secondary text-xs font-semibold border border-surface-border transition-colors"
        >
          Autocompletar
        </button>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-xs font-semibold text-text-muted mb-1.5 uppercase tracking-wider">
            Usuario o Correo
          </label>
          <input
            v-model="email"
            type="text"
            required
            placeholder="admin o admin@dramavivo.com"
            class="w-full px-4 py-3 bg-surface border border-surface-border rounded-xl text-white text-sm focus:outline-none focus:border-primary transition-colors"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-text-muted mb-1.5 uppercase tracking-wider">
            Contraseña
          </label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="••••••••"
            class="w-full px-4 py-3 bg-surface border border-surface-border rounded-xl text-white text-sm focus:outline-none focus:border-primary transition-colors"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3.5 rounded-xl bg-primary hover:bg-primary-hover text-white text-sm font-bold shadow-glow-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <div
            v-if="loading"
            class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"
          ></div>
          <span>Ingresar al Panel Maestro</span>
        </button>
      </form>

      <!-- Back Link -->
      <div class="text-center pt-2">
        <router-link to="/" class="text-xs text-text-muted hover:text-white transition-colors">
          ← Volver a la plataforma pública
        </router-link>
      </div>
    </div>
  </div>
</template>
