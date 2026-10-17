<script setup lang="ts">
import type { Series } from '../../types'
import SeriesCard from './SeriesCard.vue'

withDefaults(
  defineProps<{
    series: Series[]
    loading?: boolean
    emptyMessage?: string
    aspectRatio?: '2/3' | '9/16'
    columns?: 2 | 3 | 4 | 5 | 6
  }>(),
  {
    loading: false,
    emptyMessage: 'No se encontraron series que coincidan con los criterios.',
    aspectRatio: '2/3',
    columns: 4,
  }
)
</script>

<template>
  <div class="w-full">
    <!-- Loading skeleton -->
    <div
      v-if="loading"
      class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4 md:gap-6"
    >
      <div
        v-for="n in 8"
        :key="n"
        class="flex flex-col rounded-2xl overflow-hidden bg-surface border border-surface-border animate-pulse"
      >
        <div class="w-full aspect-[2/3] bg-surface-light"></div>
        <div class="p-4 space-y-2.5">
          <div class="h-3 bg-surface-lighter rounded w-1/3"></div>
          <div class="h-4 bg-surface-lighter rounded w-4/5"></div>
          <div class="h-3 bg-surface-lighter rounded w-full"></div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div
      v-else-if="series.length === 0"
      class="flex flex-col items-center justify-center py-16 px-4 text-center rounded-2xl bg-surface/50 border border-surface-border"
    >
      <div class="w-16 h-16 rounded-2xl bg-surface-light flex items-center justify-center text-text-muted mb-4">
        <svg class="w-8 h-8 text-text-dim" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
        </svg>
      </div>
      <h3 class="text-base font-semibold text-white mb-1">Sin resultados</h3>
      <p class="text-sm text-text-muted max-w-md">
        {{ emptyMessage }}
      </p>
    </div>

    <!-- Actual grid -->
    <div
      v-else
      class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4 md:gap-6"
    >
      <SeriesCard
        v-for="item in series"
        :key="item.id"
        :series="item"
        :aspectRatio="aspectRatio"
      />
    </div>
  </div>
</template>
