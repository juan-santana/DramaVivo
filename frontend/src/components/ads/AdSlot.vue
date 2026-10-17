<script setup lang="ts">
import { ref } from 'vue'

withDefaults(
  defineProps<{
    slotId?: string
    format?: 'banner' | 'interstitial' | 'native'
    enabled?: boolean
  }>(),
  {
    slotId: 'drama-ad-default',
    format: 'banner',
    enabled: true,
  }
)

const dismissed = ref(false)
</script>

<template>
  <div
    v-if="enabled && !dismissed"
    class="relative w-full overflow-hidden rounded-xl bg-surface/70 border border-surface-border p-3 sm:p-4 transition-all"
  >
    <!-- Ad label -->
    <div class="flex items-center justify-between mb-2">
      <span class="text-[9px] uppercase tracking-wider text-text-dim border border-surface-border px-1 rounded">
        Publicidad Patrocinada
      </span>
      <button
        @click="dismissed = true"
        class="text-text-dim hover:text-white p-0.5 rounded text-xs"
        aria-label="Cerrar anuncio"
      >
        ×
      </button>
    </div>

    <!-- Ad content slot -->
    <slot>
      <div class="flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-gradient-to-tr from-secondary/30 to-secondary/10 border border-secondary/30 flex items-center justify-center text-secondary shrink-0">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
            </svg>
          </div>
          <div>
            <h5 class="text-xs font-bold text-white">DramaApp VIP Pass</h5>
            <p class="text-[11px] text-text-muted">Desbloquea todos los microdramas sin anuncios ni esperas.</p>
          </div>
        </div>
        <router-link
          to="/catalogo"
          class="shrink-0 px-3 py-1.5 rounded-lg bg-secondary/20 hover:bg-secondary/30 border border-secondary/40 text-secondary text-xs font-semibold transition-colors"
        >
          Ver más
        </router-link>
      </div>
    </slot>
  </div>
</template>
