<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAdminStore } from '../../stores/admin'
import { useToast } from '../../composables/useToast'
import StatusBadge from '../../components/admin/StatusBadge.vue'
import LoadingSpinner from '../../components/common/LoadingSpinner.vue'
import type { DiscoveredSeries } from '../../types'

const adminStore = useAdminStore()
const toast = useToast()

const filterStatus = ref<'all' | 'pending' | 'imported' | 'blocked'>('pending')

onMounted(() => {
  adminStore.fetchDiscovered()
})

const filteredDiscovered = computed(() => {
  if (filterStatus.value === 'all') return adminStore.discovered
  return adminStore.discovered.filter(d => d.status === filterStatus.value)
})

async function handleImport(item: DiscoveredSeries) {
  toast.info(`Importando "${item.title}" al catálogo oficial...`)
  await adminStore.importDiscovered(item.id)
  toast.success(`"${item.title}" ha sido importada exitosamente.`)
}

async function handleBlock(item: DiscoveredSeries) {
  await adminStore.blockDiscovered(item.id)
  toast.warning(`"${item.title}" ha sido bloqueada.`)
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Catálogo Descubierto
        </h1>
        <p class="text-xs sm:text-sm text-text-muted mt-0.5">
          Revisa las series detectadas por los scrapers y decide cuáles publicar en DramaApp.
        </p>
      </div>

      <!-- Filter Tabs -->
      <div class="flex items-center gap-1.5 p-1 rounded-xl bg-surface border border-surface-border">
        <button
          @click="filterStatus = 'pending'"
          :class="[
            'px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors',
            filterStatus === 'pending' ? 'bg-primary text-white' : 'text-text-muted hover:text-white'
          ]"
        >
          Pendientes ({{ adminStore.discovered.filter(d => d.status === 'pending').length }})
        </button>
        <button
          @click="filterStatus = 'all'"
          :class="[
            'px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors',
            filterStatus === 'all' ? 'bg-surface-lighter text-white' : 'text-text-muted hover:text-white'
          ]"
        >
          Todas
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="adminStore.loading" class="py-12">
      <LoadingSpinner text="Consultando títulos descubiertos..." />
    </div>

    <!-- Empty State -->
    <div
      v-else-if="filteredDiscovered.length === 0"
      class="glass-panel p-12 text-center rounded-2xl border border-surface-border space-y-3"
    >
      <div class="text-3xl">🎉</div>
      <h3 class="text-base font-bold text-white">Bandeja de entrada despejada</h3>
      <p class="text-xs text-text-muted">No hay series descubiertas con el filtro seleccionado.</p>
    </div>

    <!-- Grid of Discovered Cards -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
      <div
        v-for="item in filteredDiscovered"
        :key="item.id"
        class="glass-panel rounded-2xl border border-surface-border overflow-hidden flex flex-col justify-between p-4 space-y-4 hover:border-surface-lighter transition-all"
      >
        <div class="flex gap-4">
          <div class="w-24 aspect-[2/3] rounded-xl overflow-hidden bg-surface-light shrink-0">
            <img :src="item.posterUrl" :alt="item.title" class="w-full h-full object-cover" />
          </div>

          <div class="flex-1 min-w-0 space-y-1.5">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-mono text-text-dim">Ext ID: {{ item.externalId }}</span>
              <StatusBadge :status="item.status" />
            </div>

            <h4 class="text-sm font-bold text-white leading-snug line-clamp-2">
              {{ item.title }}
            </h4>

            <p class="text-[11px] text-text-muted">
              Fuente: <span class="text-white">{{ item.sourceName }}</span>
            </p>

            <p class="text-[11px] text-text-muted">
              Episodios detectados: <span class="text-white font-mono font-bold">{{ item.episodeCount }}</span>
            </p>

            <p class="text-xs text-text-dim line-clamp-2">
              {{ item.synopsis }}
            </p>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="pt-3 border-t border-surface-border flex items-center justify-end gap-2">
          <button
            v-if="item.status !== 'blocked'"
            @click="handleBlock(item)"
            class="px-3 py-1.5 rounded-lg bg-red-950/40 hover:bg-red-950/80 text-red-300 text-xs font-semibold border border-red-800/40 transition-colors"
          >
            Bloquear
          </button>

          <button
            v-if="item.status !== 'imported'"
            @click="handleImport(item)"
            class="px-4 py-1.5 rounded-lg bg-primary hover:bg-primary-hover text-white text-xs font-bold shadow-glow-primary transition-all flex items-center gap-1.5"
          >
            <span>+ Importar a Catálogo</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
