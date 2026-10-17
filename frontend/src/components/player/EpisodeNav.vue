<script setup lang="ts">
import type { Episode } from '../../types'

defineProps<{
  hasPrev: boolean
  hasNext: boolean
  prevEpisode?: Episode | null
  nextEpisode?: Episode | null
}>()

const emit = defineEmits<{
  (e: 'prev'): void
  (e: 'next'): void
}>()
</script>

<template>
  <div class="flex items-center gap-2">
    <!-- Prev Episode -->
    <button
      @click="emit('prev')"
      :disabled="!hasPrev"
      :class="[
        'flex items-center gap-1 px-3 py-2 rounded-xl text-xs font-semibold backdrop-blur-md transition-all',
        hasPrev
          ? 'bg-black/60 hover:bg-black/80 text-white border border-white/10 shadow-md'
          : 'bg-black/30 text-white/30 cursor-not-allowed border border-transparent'
      ]"
      :title="prevEpisode ? `Episodio ${prevEpisode.episodeNumber}: ${prevEpisode.title}` : 'Capítulo anterior'"
    >
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      <span class="hidden sm:inline">Anterior</span>
    </button>

    <!-- Next Episode -->
    <button
      @click="emit('next')"
      :disabled="!hasNext"
      :class="[
        'flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold backdrop-blur-md transition-all',
        hasNext
          ? 'bg-primary hover:bg-primary-hover text-white shadow-glow-primary'
          : 'bg-black/30 text-white/30 cursor-not-allowed border border-transparent'
      ]"
      :title="nextEpisode ? `Episodio ${nextEpisode.episodeNumber}: ${nextEpisode.title}` : 'Siguiente capítulo'"
    >
      <span>Siguiente</span>
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </div>
</template>
