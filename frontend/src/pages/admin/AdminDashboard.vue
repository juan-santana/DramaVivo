<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '../../stores/admin'
import StatsCard from '../../components/admin/StatsCard.vue'
import StatusBadge from '../../components/admin/StatusBadge.vue'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'

const router = useRouter()
const adminStore = useAdminStore()

onMounted(async () => {
  await Promise.all([
    adminStore.fetchSeries(),
    adminStore.fetchSources(),
    adminStore.fetchRights(),
    adminStore.fetchImportJobs(),
    adminStore.fetchAnalytics(),
  ])
})

function navigateTo(path: string) {
  router.push(path)
}
</script>

<template>
  <div class="space-y-8">
    <!-- Header banner -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Panel de Control General
        </h1>
        <p class="text-xs sm:text-sm text-text-muted mt-0.5">
          Resumen operativo del motor de microdramas, flujos de importación y licencias.
        </p>
      </div>

      <!-- Quick Actions Dropdown / Buttons -->
      <div class="flex items-center gap-2">
        <button
          @click="navigateTo('/admin/series')"
          class="px-4 py-2 rounded-xl bg-primary hover:bg-primary-hover text-white text-xs font-bold shadow-glow-primary transition-all flex items-center gap-1.5"
        >
          <span>+ Nueva Serie</span>
        </button>
        <button
          @click="navigateTo('/admin/fuentes')"
          class="px-3.5 py-2 rounded-xl bg-surface-light hover:bg-surface-lighter text-text-muted hover:text-white text-xs font-semibold border border-surface-border transition-colors"
        >
          Ejecutar Scraper
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="adminStore.loading && adminStore.series.length === 0" class="py-12">
      <LoadingSpinner text="Cargando estadísticas operativas..." />
    </div>

    <template v-else>
      <!-- Stats Cards Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <StatsCard
          title="Total de Series"
          :value="adminStore.series.length || 90"
          change="+12% este mes"
          :isPositive="true"
          iconColor="primary"
        >
          <template #icon>
            <svg class="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          title="Episodios Catalogados"
          :value="(adminStore.analytics?.totalEpisodes || 1426).toLocaleString('es-ES')"
          change="Streaming activo"
          :isPositive="true"
          iconColor="secondary"
        >
          <template #icon>
            <svg class="w-6 h-6 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          title="Fuentes de Raspado"
          :value="adminStore.sources.length || 6"
          change="6 configuradas"
          :isPositive="true"
          iconColor="blue"
        >
          <template #icon>
            <svg class="w-6 h-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </template>
        </StatsCard>

        <StatsCard
          title="Reproducciones Totales"
          :value="(adminStore.analytics?.totalViews || 115936090).toLocaleString('es-ES')"
          change="+18.4% semanal"
          :isPositive="true"
          iconColor="green"
        >
          <template #icon>
            <svg class="w-6 h-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </template>
        </StatsCard>
      </div>

      <!-- Quick Actions Grid -->
      <section class="space-y-3">
        <h3 class="text-sm font-bold text-white uppercase tracking-wider">Acciones Rápidas</h3>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <button
            @click="navigateTo('/admin/fuentes')"
            class="p-4 rounded-2xl glass-panel border border-surface-border hover:border-primary/50 text-left transition-all group"
          >
            <span class="text-xl block mb-2 group-hover:scale-110 transition-transform">⚙️</span>
            <span class="text-xs font-bold text-white block">Fuentes Scraper</span>
            <span class="text-[11px] text-text-muted">Añadir o ejecutar recolectores</span>
          </button>

          <button
            @click="navigateTo('/admin/descubiertos')"
            class="p-4 rounded-2xl glass-panel border border-surface-border hover:border-primary/50 text-left transition-all group"
          >
            <span class="text-xl block mb-2 group-hover:scale-110 transition-transform">🔍</span>
            <span class="text-xs font-bold text-white block">Catálogo Descubierto</span>
            <span class="text-[11px] text-text-muted">Aprobar series entrantes</span>
          </button>

          <button
            @click="navigateTo('/admin/derechos')"
            class="p-4 rounded-2xl glass-panel border border-surface-border hover:border-primary/50 text-left transition-all group"
          >
            <span class="text-xl block mb-2 group-hover:scale-110 transition-transform">🛡️</span>
            <span class="text-xs font-bold text-white block">Gestión Legal</span>
            <span class="text-[11px] text-text-muted">Revisar licencias y contratos</span>
          </button>

          <button
            @click="navigateTo('/admin/videos')"
            class="p-4 rounded-2xl glass-panel border border-surface-border hover:border-primary/50 text-left transition-all group"
          >
            <span class="text-xl block mb-2 group-hover:scale-110 transition-transform">📹</span>
            <span class="text-xs font-bold text-white block">Videos y Transcoding</span>
            <span class="text-[11px] text-text-muted">Subir nuevos archivos HLS</span>
          </button>
        </div>
      </section>

      <!-- Recent Import Activity & Series -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Recent Import Jobs -->
        <div class="glass-panel p-5 rounded-2xl border border-surface-border space-y-4">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-bold text-white">Últimos Trabajos de Importación</h4>
            <router-link to="/admin/trabajos" class="text-xs text-primary font-semibold hover:underline">
              Ver todos →
            </router-link>
          </div>

          <div class="space-y-2.5">
            <div
              v-for="job in adminStore.importJobs.slice(0, 4)"
              :key="job.id"
              class="p-3 rounded-xl bg-surface/60 border border-surface-border flex items-center justify-between text-xs"
            >
              <div>
                <p class="font-bold text-white">{{ job.sourceName }}</p>
                <p class="text-[11px] text-text-muted">
                  {{ job.recordsImported }} importadas • {{ job.recordsDiscovered }} descubiertas
                </p>
              </div>
              <StatusBadge :status="job.status" />
            </div>
          </div>
        </div>

        <!-- Pending Rights Records -->
        <div class="glass-panel p-5 rounded-2xl border border-surface-border space-y-4">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-bold text-white">Revisión de Derechos Pendientes</h4>
            <router-link to="/admin/derechos" class="text-xs text-primary font-semibold hover:underline">
              Ver todos →
            </router-link>
          </div>

          <div class="space-y-2.5">
            <div
              v-for="right in adminStore.rights.slice(0, 4)"
              :key="right.id"
              class="p-3 rounded-xl bg-surface/60 border border-surface-border flex items-center justify-between text-xs"
            >
              <div>
                <p class="font-bold text-white">{{ right.seriesTitle }}</p>
                <p class="text-[11px] text-text-muted">Titular: {{ right.holderName }}</p>
              </div>
              <StatusBadge :status="right.status" />
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
