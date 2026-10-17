<script setup lang="ts">
import { computed } from 'vue'
import type { Episode } from '../../types'

const props = defineProps<{
  episode: Episode
  isActive?: boolean
}>()

const formattedDuration = computed(() => {
  const m = Math.floor(props.episode.duration / 60)
  const s = props.episode.duration % 60
  return `${m}:${s < 10 ? '0' : ''}${s}`
})
</script>

<template>
  <div
    :class="[
      'group relative flex items-center gap-3 sm:gap-4 p-2.5 sm:p-3 rounded-xl border transition-all duration-200 cursor-pointer',
      isActive
        ? 'bg-primary/10 border-primary/40 shadow-glow-primary'
        : 'bg-surface/60 hover:bg-surface border-surface-border'
    ]"
  >
    <!-- Thumbnail -->
    <div class="relative w-24 sm:w-28 aspect-video rounded-lg overflow-hidden bg-surface-light shrink-0">
      <img
        :src="episode.thumbnailUrl"
        :alt="episode.title"
        loading="lazy"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      />
      <div class="absolute inset-0 bg-black/40 group-hover:bg-black/20 flex items-center justify-center transition-colors">
        <div
          :class="[
            'w-7 h-7 rounded-full flex items-center justify-center transition-transform',
            isActive ? 'bg-primary text-white scale-110' : 'bg-black/60 text-white/90 group-hover:scale-110'
          ]"
        >
          <svg class="w-3.5 h-3.5 fill-current translate-x-0.5" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
        </div>
      </div>

      <!-- Duration badge -->
      <span class="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-black/80 backdrop-blur-sm text-[10px] font-mono text-white/90">
        {{ formattedDuration }}
      </span>
    </div>

    <!-- Episode Details -->
    <div class="flex-1 min-w-0">
      <div class="flex items-center gap-2 mb-1">
        <span class="text-xs font-bold font-mono text-primary">
          EP {{ episode.episodeNumber }}
        </span>
        <span
          v-if="episode.isFree"
          class="text-[10px] font-semibold px-1.5 py-0.2 rounded bg-green-950/80 text-green-300 border border-green-700/30"
        >
          GRATIS
        </span>
      </div>

      <h4
        :class="[
          'text-sm font-semibold truncate transition-colors',
          isActive ? 'text-primary' : 'text-white group-hover:text-primary-light'
        ]"
      >
        {{ episode.title }}
      </h4>

      <p v-if="episode.synopsis" class="text-xs text-text-muted line-clamp-1 mt-0.5">
        {{ episode.synopsis }}
      </p>
    </div>
  </div>
</template>
