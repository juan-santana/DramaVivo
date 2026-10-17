<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { useFavoritesStore } from '../../stores/favorites'
import { useI18n } from '../../i18n'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const favoritesStore = useFavoritesStore()
const { t, currentLang, setLocale } = useI18n()

const mobileMenuOpen = ref(false)

const navLinks = computed(() => [
  { name: t('nav.home'), path: '/' },
  { name: t('nav.catalog'), path: '/catalogo' },
  { name: t('nav.myList'), path: '/mi-lista', badge: favoritesStore.favorites.length },
  { name: t('nav.search'), path: '/buscar' },
])

function isActive(path: string) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

function navigateTo(path: string) {
  mobileMenuOpen.value = false
  router.push(path)
}
</script>

<template>
  <header class="sticky top-0 z-40 w-full bg-background/25 backdrop-blur-2xl border-b border-white/5 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 sm:h-20">
        <!-- Brand / Logo (DramaVivo) -->
        <router-link to="/" class="flex items-center gap-3 group">
          <!-- Custom Futuristic DramaVivo Emblem (Replaces generic red button) -->
          <div class="relative w-9 h-9 sm:w-10 sm:h-10 flex items-center justify-center">
            <div class="absolute inset-0 bg-gradient-to-tr from-rose-500 via-amber-400 to-purple-600 rounded-2xl blur-[6px] opacity-70 group-hover:opacity-100 transition-opacity"></div>
            <div class="relative w-9 h-9 sm:w-10 sm:h-10 rounded-2xl bg-[#12121a]/90 border border-white/20 p-2 flex items-center justify-center backdrop-blur-md group-hover:scale-105 transition-transform shadow-lg">
              <svg class="w-full h-full" viewBox="0 0 32 32" fill="none">
                <path d="M6 7L16 25L26 7" stroke="url(#dv-gradient-1)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M11 7L16 16L21 7" stroke="url(#dv-gradient-2)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
                <circle cx="16" cy="16" r="2.2" fill="#F5C518" />
                <defs>
                  <linearGradient id="dv-gradient-1" x1="6" y1="7" x2="26" y2="25" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#FF2E55" />
                    <stop offset="0.5" stop-color="#FF9E00" />
                    <stop offset="1" stop-color="#9333EA" />
                  </linearGradient>
                  <linearGradient id="dv-gradient-2" x1="11" y1="7" x2="21" y2="16" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#FFD700" />
                    <stop offset="1" stop-color="#FF2E55" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </div>

          <div class="flex flex-col">
            <span class="text-xl sm:text-2xl font-black tracking-tight text-white flex items-center">
              Drama<span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-rose-500 to-purple-400 font-black ml-0.5">Vivo</span>
            </span>
            <span class="text-[9px] tracking-[0.25em] text-text-muted/90 uppercase font-bold -mt-1 flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              STREAMING HD
            </span>
          </div>
        </router-link>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center space-x-1 lg:space-x-2">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            :class="[
              'px-3.5 py-2 rounded-xl text-sm font-medium transition-all duration-200 flex items-center gap-1.5',
              isActive(link.path)
                ? 'text-white bg-surface-light border border-surface-border shadow-sm'
                : 'text-text-muted hover:text-white hover:bg-surface-light/50'
            ]"
          >
            <span>{{ link.name }}</span>
            <span
              v-if="link.badge"
              class="px-1.5 py-0.2 text-[10px] font-black rounded-full bg-primary/20 text-primary border border-primary/30 font-mono"
            >
              {{ link.badge }}
            </span>
          </router-link>
        </nav>

        <!-- Right Side Actions -->
        <div class="hidden md:flex items-center space-x-3">
          <!-- Language Switcher Pill -->
          <div class="flex items-center bg-surface-dark border border-surface-border rounded-xl p-0.5 text-xs font-bold tracking-wider">
            <button
              @click="setLocale('es')"
              :class="[
                'px-2.5 py-1 rounded-lg transition-all',
                currentLang === 'es'
                  ? 'bg-primary text-white shadow-sm'
                  : 'text-text-muted hover:text-white'
              ]"
              title="Español"
            >
              ES
            </button>
            <button
              @click="setLocale('en')"
              :class="[
                'px-2.5 py-1 rounded-lg transition-all',
                currentLang === 'en'
                  ? 'bg-primary text-white shadow-sm'
                  : 'text-text-muted hover:text-white'
              ]"
              title="English"
            >
              EN
            </button>
          </div>

          <!-- Search button shortcut -->
          <router-link
            to="/buscar"
            class="p-2.5 rounded-xl text-text-muted hover:text-white hover:bg-surface-light transition-colors"
            title="Buscar dramas"
            aria-label="Buscar"
          >
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </router-link>

          <!-- Admin Portal Link -->
          <router-link
            :to="authStore.isAuthenticated ? '/admin' : '/admin/login'"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg border border-surface-border text-text-muted hover:text-secondary hover:border-secondary/50 hover:bg-surface-light transition-all"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <span>Admin</span>
          </router-link>
        </div>

        <!-- Mobile Menu Trigger -->
        <div class="flex md:hidden items-center gap-2">
          <!-- Mobile Language Pill -->
          <div class="flex items-center bg-surface-dark border border-surface-border rounded-lg p-0.5 text-[11px] font-bold">
            <button
              @click="setLocale('es')"
              :class="[
                'px-2 py-0.5 rounded transition-all',
                currentLang === 'es' ? 'bg-primary text-white' : 'text-text-muted'
              ]"
            >
              ES
            </button>
            <button
              @click="setLocale('en')"
              :class="[
                'px-2 py-0.5 rounded transition-all',
                currentLang === 'en' ? 'bg-primary text-white' : 'text-text-muted'
              ]"
            >
              EN
            </button>
          </div>

          <router-link
            to="/buscar"
            class="p-2 text-text-muted hover:text-white"
            aria-label="Buscar"
          >
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </router-link>

          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="p-2 text-text-muted hover:text-white rounded-lg focus:outline-none"
            aria-label="Abrir menú de navegación"
          >
            <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation Drawer -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="-translate-y-4 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="-translate-y-4 opacity-0"
    >
      <div
        v-if="mobileMenuOpen"
        class="md:hidden glass-panel border-t border-b border-surface-border px-4 pt-3 pb-6 space-y-2 shadow-2xl"
      >
        <button
          v-for="link in navLinks"
          :key="link.path"
          @click="navigateTo(link.path)"
          :class="[
            'w-full text-left px-4 py-3 rounded-xl text-base font-medium flex items-center justify-between transition-colors',
            isActive(link.path)
              ? 'bg-primary/20 text-white border border-primary/30'
              : 'text-text-muted hover:text-white hover:bg-surface-light'
          ]"
        >
          <div class="flex items-center gap-2">
            <span>{{ link.name }}</span>
            <span
              v-if="link.badge"
              class="px-2 py-0.5 text-xs font-black rounded-full bg-primary/20 text-primary border border-primary/30 font-mono"
            >
              {{ link.badge }}
            </span>
          </div>
          <svg class="w-4 h-4 text-text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>

        <div class="pt-3 border-t border-surface-border flex items-center justify-between px-2">
          <span class="text-xs text-text-muted font-medium">{{ t('nav.language') }}</span>
          <div class="flex items-center bg-surface-dark border border-surface-border rounded-lg p-0.5 text-xs font-bold">
            <button
              @click="setLocale('es')"
              :class="[
                'px-3 py-1 rounded transition-all',
                currentLang === 'es' ? 'bg-primary text-white shadow-sm' : 'text-text-muted'
              ]"
            >
              Español
            </button>
            <button
              @click="setLocale('en')"
              :class="[
                'px-3 py-1 rounded transition-all',
                currentLang === 'en' ? 'bg-primary text-white shadow-sm' : 'text-text-muted'
              ]"
            >
              English
            </button>
          </div>
        </div>

        <div class="pt-2">
          <button
            @click="navigateTo(authStore.isAuthenticated ? '/admin' : '/admin/login')"
            class="w-full text-left px-4 py-3 rounded-xl text-sm font-semibold text-secondary hover:bg-surface-light flex items-center justify-between"
          >
            <span>Panel de Administración</span>
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </header>
</template>
