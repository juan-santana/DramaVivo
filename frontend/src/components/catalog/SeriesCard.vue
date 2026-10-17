<script setup lang="ts">
import { computed } from 'vue'
import type { Series } from '../../types'
import { useFavoritesStore } from '../../stores/favorites'
import { useI18n } from '../../i18n'

const props = defineProps<{
  series: Series
  aspectRatio?: '2/3' | '9/16'
}>()

const favoritesStore = useFavoritesStore()
const { t, currentLang } = useI18n()
const isFav = computed(() => favoritesStore.isFavorite(props.series.id))

function toggleFav(e: Event) {
  e.preventDefault()
  e.stopPropagation()
  favoritesStore.toggleFavorite(props.series)
}
</script>

<template>
  <router-link
    :to="`/serie/${series.slug || series.id}`"
    class="group relative flex flex-col rounded-2xl overflow-hidden bg-surface border border-surface-border card-hover-glow cursor-pointer transition-all duration-300"
  >
    <!-- Poster Container -->
    <div
      :class="[
        'relative w-full overflow-hidden bg-surface-light',
        aspectRatio === '9/16' ? 'aspect-[9/16]' : 'aspect-[2/3]'
      ]"
    >
      <img
        :src="series.verticalPosterUrl || series.posterUrl"
        :alt="series.title"
        loading="lazy"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
      />

      <!-- Dark Gradient Overlay -->
      <div class="absolute inset-0 bg-gradient-to-t from-background via-black/20 to-transparent opacity-80 group-hover:opacity-60 transition-opacity"></div>

      <!-- Top Badges: Favorite & Rating -->
      <div class="absolute top-2.5 inset-x-2.5 flex items-center justify-between z-10">
        <span
          v-if="series.rating"
          class="flex items-center gap-1 px-2 py-0.5 rounded-md bg-black/60 backdrop-blur-md text-[11px] font-bold text-secondary border border-secondary/20 shadow-sm"
        >
          <svg class="w-3 h-3 fill-current text-secondary" viewBox="0 0 24 24">
            <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
          </svg>
          {{ series.rating.toFixed(1) }}
        </span>
        <span v-else></span>

        <button
          @click="toggleFav"
          :class="[
            'p-1.5 rounded-full backdrop-blur-md transition-all shadow-md flex items-center justify-center',
            isFav
              ? 'bg-secondary text-black scale-110 shadow-glow-gold'
              : 'bg-black/60 text-white/80 hover:text-white hover:bg-black/90'
          ]"
          :title="isFav ? 'Quitar de Mi Lista' : 'Guardar en Mi Lista'"
          aria-label="Mi Lista"
        >
          <svg class="w-4 h-4" :fill="isFav ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0z" />
          </svg>
        </button>
      </div>

      <!-- Center Play Overlay on Hover -->
      <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 transform scale-90 group-hover:scale-100 pointer-events-none">
        <div class="w-12 h-12 rounded-full bg-primary/90 text-white flex items-center justify-center shadow-glow-primary">
          <svg class="w-6 h-6 fill-current translate-x-0.5" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
        </div>
      </div>

      <!-- Bottom Badges inside poster -->
      <div class="absolute bottom-2.5 left-2.5 right-2.5 flex items-center justify-between text-[11px] font-medium text-white/90">
        <span class="px-2 py-0.5 rounded-md bg-black/70 backdrop-blur-md font-mono">
          {{ currentLang === 'en' ? `${series.totalEpisodes || 1} eps` : `${series.totalEpisodes || 1} eps` }}
        </span>
        <span v-if="series.status === 'completed'" class="px-1.5 py-0.5 rounded-md bg-green-950/80 text-green-300 border border-green-700/30 text-[10px]">
          {{ currentLang === 'en' ? 'Completed' : 'Completa' }}
        </span>
        <span v-else class="px-1.5 py-0.5 rounded-md bg-red-950/80 text-primary-light border border-primary/30 text-[10px]">
          {{ currentLang === 'en' ? 'Ongoing' : 'En emisión' }}
        </span>
      </div>
    </div>

    <!-- Info Section -->
    <div class="p-3 sm:p-4 flex flex-col flex-1 justify-between gap-2">
      <div>
        <!-- Genres -->
        <div class="flex flex-wrap gap-1.5 mb-1.5">
          <span
            v-for="genre in series.genres.slice(0, 2)"
            :key="genre"
            class="text-[10px] font-semibold uppercase tracking-wider text-text-muted/80 bg-surface-lighter px-1.5 py-0.5 rounded"
          >
            {{ genre }}
          </span>
        </div>

        <!-- Title -->
        <h3 class="text-sm font-bold text-white group-hover:text-primary transition-colors line-clamp-1 leading-snug">
          {{ currentLang === 'en' && series.originalTitle ? series.originalTitle : series.title }}
        </h3>
      </div>

      <!-- Synopsis preview -->
      <p class="text-xs text-text-muted line-clamp-2 leading-relaxed">
        {{ series.synopsis }}
      </p>
    </div>
  </router-link>
</template>
