<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Toast from '../components/common/Toast.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const sidebarOpen = ref(false)

const navItems = [
  {
    name: 'Dashboard',
    path: '/admin',
    icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
  },
  {
    name: 'Fuentes Scraper',
    path: '/admin/fuentes',
    icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10',
  },
  {
    name: 'Trabajos de Importación',
    path: '/admin/trabajos',
    icon: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15',
  },
  {
    name: 'Catálogo Descubierto',
    path: '/admin/descubiertos',
    icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z',
  },
  {
    name: 'Gestión de Derechos',
    path: '/admin/derechos',
    icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
  },
  {
    name: 'Series y Catálogo',
    path: '/admin/series',
    icon: 'M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z',
  },
  {
    name: 'Episodios',
    path: '/admin/episodios',
    icon: 'M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z',
  },
  {
    name: 'Videos y Medios',
    path: '/admin/videos',
    icon: 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z',
  },
  {
    name: 'Reclamaciones DMCA',
    path: '/admin/reclamaciones',
    icon: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
  },
  {
    name: 'Analítica y Audiencia',
    path: '/admin/analitica',
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
  },
]

function isCurrent(path: string) {
  if (path === '/admin') return route.path === '/admin'
  return route.path.startsWith(path)
}

async function handleLogout() {
  await authStore.logout()
  router.push('/admin/login')
}
</script>

<template>
  <div class="min-h-screen bg-background flex flex-col md:flex-row text-text-main">
    <!-- Mobile top bar -->
    <div class="md:hidden glass-header flex items-center justify-between p-4 sticky top-0 z-40">
      <router-link to="/admin" class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-rose-500 via-amber-400 to-purple-600 flex items-center justify-center p-0.5 shadow-glow-primary">
          <div class="w-full h-full bg-[#12121a] rounded-[6px] flex items-center justify-center text-white font-black text-xs">
            DV
          </div>
        </div>
        <span class="font-black text-white text-base">Drama<span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-rose-500 to-purple-400">Vivo</span> <span class="text-secondary text-xs font-mono font-bold">Admin</span></span>
      </router-link>

      <button
        @click="sidebarOpen = !sidebarOpen"
        class="p-2 rounded-lg bg-surface-light text-text-muted hover:text-white"
        aria-label="Abrir panel"
      >
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>

    <!-- Sidebar backdrop for mobile -->
    <div
      v-if="sidebarOpen"
      @click="sidebarOpen = false"
      class="fixed inset-0 bg-black/70 backdrop-blur-sm z-40 md:hidden"
    ></div>

    <!-- Sidebar navigation -->
    <aside
      :class="[
        'fixed inset-y-0 left-0 z-50 w-64 glass-panel border-r border-surface-border flex flex-col justify-between transition-transform duration-300 md:static md:translate-x-0',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
      ]"
    >
      <div>
        <!-- Logo -->
        <div class="p-6 border-b border-surface-border flex items-center justify-between">
          <router-link to="/admin" class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-rose-500 via-amber-400 to-purple-600 flex items-center justify-center p-0.5 shadow-glow-primary">
              <div class="w-full h-full bg-[#12121a] rounded-[10px] flex items-center justify-center text-white font-black text-xs">
                DV
              </div>
            </div>
            <div>
              <h2 class="text-base font-black text-white leading-tight">
                Drama<span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-rose-500 to-purple-400">Vivo</span>
              </h2>
              <span class="text-[10px] font-bold text-secondary uppercase tracking-wider">
                Panel Maestro
              </span>
            </div>
          </router-link>

          <button
            @click="sidebarOpen = false"
            class="md:hidden text-text-muted hover:text-white"
          >
            ✕
          </button>
        </div>

        <!-- Links List -->
        <nav class="p-3 space-y-1 overflow-y-auto max-h-[calc(100vh-210px)]">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            @click="sidebarOpen = false"
            :class="[
              'flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all',
              isCurrent(item.path)
                ? 'bg-primary text-white shadow-glow-primary'
                : 'text-text-muted hover:text-white hover:bg-surface-light'
            ]"
          >
            <svg class="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
            </svg>
            <span class="truncate">{{ item.name }}</span>
          </router-link>
        </nav>
      </div>

      <!-- Footer / User info -->
      <div class="p-4 border-t border-surface-border bg-surface/40">
        <div class="flex items-center gap-3 mb-3">
          <img
            :src="authStore.user?.avatarUrl || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80'"
            alt="Admin Avatar"
            class="w-9 h-9 rounded-full object-cover border border-secondary/50"
          />
          <div class="min-w-0 flex-1">
            <h5 class="text-xs font-bold text-white truncate">
              {{ authStore.user?.name || 'Administrador' }}
            </h5>
            <span class="text-[10px] px-1.5 py-0.2 rounded bg-secondary/20 text-secondary font-mono uppercase">
              {{ authStore.user?.role || 'Admin' }}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-2">
          <router-link
            to="/"
            class="text-center px-2 py-1.5 rounded-lg bg-surface-light hover:bg-surface-lighter text-text-muted hover:text-white text-[11px] font-medium border border-surface-border transition-colors"
          >
            Ver Web
          </router-link>
          <button
            @click="handleLogout"
            class="text-center px-2 py-1.5 rounded-lg bg-red-950/40 hover:bg-red-950/80 text-red-300 text-[11px] font-semibold border border-red-800/40 transition-colors"
          >
            Salir
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Admin Content Area -->
    <div class="flex-1 min-w-0 flex flex-col overflow-y-auto">
      <!-- Admin Topbar -->
      <header class="glass-header hidden md:flex items-center justify-between px-8 py-4 border-b border-surface-border">
        <div class="flex items-center gap-2 text-xs text-text-muted">
          <span>Administración</span>
          <span>/</span>
          <span class="text-white font-medium capitalize">{{ route.name?.toString() || 'Panel' }}</span>
        </div>

        <div class="flex items-center gap-4">
          <router-link
            to="/"
            target="_blank"
            class="flex items-center gap-1.5 text-xs text-text-muted hover:text-white transition-colors"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
            <span>Ver sitio público</span>
          </router-link>
        </div>
      </header>

      <!-- Sub Page Content -->
      <main class="flex-1 p-4 sm:p-6 lg:p-8">
        <router-view />
      </main>
    </div>

    <!-- Toast container -->
    <Toast />
  </div>
</template>
