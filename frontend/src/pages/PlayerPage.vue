<script setup lang="ts">
import { onMounted, watch, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHead } from '@unhead/vue'
import { usePlayerStore } from '../stores/player'
import { useFavoritesStore } from '../stores/favorites'
import { useI18n } from '../i18n'
import { seriesService } from '../services/series'
import VideoPlayer from '../components/player/VideoPlayer.vue'
import EpisodeNav from '../components/player/EpisodeNav.vue'
import SeriesCard from '../components/catalog/SeriesCard.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import type { Episode, Series } from '../types'

const route = useRoute()
const router = useRouter()
const playerStore = usePlayerStore()
const favoritesStore = useFavoritesStore()
const { t, currentLang } = useI18n()

const isFav = computed(() => {
  return playerStore.currentSeries ? favoritesStore.isFavorite(playerStore.currentSeries.id) : false
})

function toggleFav() {
  if (playerStore.currentSeries) {
    favoritesStore.toggleFavorite(playerStore.currentSeries)
  }
}

const relatedSeries = ref<Series[]>([])
const trendingSeries = ref<Series[]>([])
const sameSourceSeries = ref<Series[]>([])

useHead({
  title: computed(() => {
    if (playerStore.currentEpisode && playerStore.currentSeries) {
      const title = currentLang.value === 'en' && playerStore.currentSeries.originalTitle ? playerStore.currentSeries.originalTitle : playerStore.currentSeries.title
      return `Ep. ${playerStore.currentEpisode.episodeNumber} - ${title} | DramaVivo`
    }
    return 'Reproductor de Microdrama - DramaVivo'
  }),
})

async function loadRecommendations() {
  try {
    const all = await seriesService.getAll({ pageSize: 50 })
    const curId = playerStore.currentSeries?.id
    const curGenres = playerStore.currentSeries?.genres || []
    const curSource = playerStore.currentSeries?.sourceId

    // 1. Same genre / related
    relatedSeries.value = all.data
      .filter(s => s.id !== curId && s.genres.some(g => curGenres.includes(g)))
      .slice(0, 8)

    // 2. Same source platform (DramaBox, GoodShort, NetShort, etc.)
    if (curSource) {
      sameSourceSeries.value = all.data
        .filter(s => s.id !== curId && s.sourceId === curSource)
        .slice(0, 8)
    }

    // 3. Top trending
    trendingSeries.value = [...all.data]
      .filter(s => s.id !== curId)
      .sort((a, b) => (b.viewsCount || 0) - (a.viewsCount || 0))
      .slice(0, 8)
  } catch (err) {
    console.error('Error loading recommendations:', err)
  }
}

async function initializePlayer() {
  const seriesId = route.params.seriesId as string
  const episodeId = route.params.episodeId as string | undefined
  if (seriesId) {
    await playerStore.loadEpisode(seriesId, episodeId)
    await loadRecommendations()
  }
}

onMounted(() => {
  initializePlayer()
})

watch(
  () => [route.params.seriesId, route.params.episodeId],
  () => {
    initializePlayer()
  }
)

function onTimeUpdate(currentTime: number, duration: number) {
  playerStore.updateProgress(currentTime, duration)
}

function handleNext() {
  if (playerStore.nextEpisode && playerStore.currentSeries) {
    router.push(`/reproducir/${playerStore.currentSeries.id}/${playerStore.nextEpisode.id}`)
  }
}

function handlePrev() {
  if (playerStore.prevEpisode && playerStore.currentSeries) {
    router.push(`/reproducir/${playerStore.currentSeries.id}/${playerStore.prevEpisode.id}`)
  }
}

function selectEpisode(ep: Episode) {
  if (playerStore.currentSeries) {
    router.push(`/reproducir/${playerStore.currentSeries.id}/${ep.id}`)
  }
}

function goBackToSeries() {
  if (playerStore.currentSeries) {
    router.push(`/serie/${playerStore.currentSeries.slug || playerStore.currentSeries.id}`)
  } else {
    router.push('/catalogo')
  }
}
</script>

<template>
  <div class="min-h-screen bg-black text-white flex flex-col justify-between pb-12">
    <!-- Top Bar Navigation -->
    <div class="max-w-7xl mx-auto w-full px-4 sm:px-6 py-4 flex items-center justify-between">
      <button
        @click="goBackToSeries"
        class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-surface/80 hover:bg-surface border border-surface-border text-xs font-semibold text-text-muted hover:text-white transition-colors"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span>{{ t('player.back') }}</span>
      </button>

      <div class="flex items-center gap-3">
        <button
          v-if="playerStore.currentSeries"
          @click="toggleFav"
          :class="[
            'px-3 py-1.5 rounded-xl text-xs font-semibold border backdrop-blur-md transition-all flex items-center gap-1.5',
            isFav
              ? 'bg-secondary/20 border-secondary text-secondary shadow-glow-gold'
              : 'bg-surface hover:bg-surface-light border-surface-border text-white'
          ]"
          :title="isFav ? 'Quitar de Mi Lista' : 'Guardar en Mi Lista'"
        >
          <svg class="w-3.5 h-3.5" :fill="isFav ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0z" />
          </svg>
          <span class="hidden sm:inline">{{ isFav ? '✓ En Mi Lista' : '+ Mi Lista' }}</span>
        </button>

        <div class="text-right">
          <h2 class="text-xs sm:text-sm font-bold text-white truncate max-w-[150px] sm:max-w-md">
            {{ (currentLang === 'en' && playerStore.currentSeries?.originalTitle ? playerStore.currentSeries.originalTitle : playerStore.currentSeries?.title) || t('player.playing') }}
          </h2>
          <span class="text-[11px] text-primary font-mono font-semibold">
            {{ currentLang === 'en' ? `Episode ${playerStore.currentEpisode?.episodeNumber || 1} of ${playerStore.episodesQueue.length}` : `Episodio ${playerStore.currentEpisode?.episodeNumber || 1} de ${playerStore.episodesQueue.length}` }}
          </span>
        </div>
      </div>
    </div>

    <!-- Main Player Stage -->
    <div class="max-w-7xl mx-auto w-full px-4 sm:px-6 flex-1 flex flex-col lg:flex-row items-center lg:items-start justify-center gap-8 py-2">
      <!-- Loading State -->
      <div v-if="playerStore.loading" class="w-full aspect-[9/16] max-w-sm flex items-center justify-center bg-surface rounded-2xl">
        <LoadingSpinner size="lg" text="Iniciando transmisión..." />
      </div>

      <!-- Video Player Component -->
      <div
        v-else-if="playerStore.currentEpisode"
        class="flex flex-col items-center gap-4 w-full max-w-sm sm:max-w-md transition-all duration-300"
      >
        <VideoPlayer
          :episode="playerStore.currentEpisode"
          :seriesTitle="currentLang === 'en' && playerStore.currentSeries?.originalTitle ? playerStore.currentSeries.originalTitle : playerStore.currentSeries?.title"
          :initialTime="playerStore.currentTime"
          @timeupdate="onTimeUpdate"
          @ended="handleNext"
          @next="handleNext"
          @prev="handlePrev"
        />

        <!-- Episode Navigation Toolbar (Only shown if series has multiple episodes) -->
        <div v-if="playerStore.episodesQueue.length > 1" class="w-full flex items-center justify-between px-2">
          <span class="text-xs text-text-muted">
            {{ currentLang === 'en' ? 'Quality' : 'Calidad' }}: <span class="text-white font-mono font-bold">1080p HD</span>
          </span>

          <EpisodeNav
            :hasPrev="playerStore.hasPrev"
            :hasNext="playerStore.hasNext"
            :prevEpisode="playerStore.prevEpisode"
            :nextEpisode="playerStore.nextEpisode"
            @prev="handlePrev"
            @next="handleNext"
          />
        </div>
      </div>

      <!-- Episode Drawer / Quick Switcher (Desktop & Mobile) -->
      <div
        v-if="playerStore.episodesQueue.length > 1"
        class="w-full max-w-md lg:w-96 glass-panel rounded-2xl border border-surface-border p-4 flex flex-col max-h-[600px] overflow-hidden"
      >
        <div class="flex items-center justify-between pb-3 border-b border-surface-border">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <span>{{ t('series.episodesList') }}</span>
            <span class="text-[11px] px-2 py-0.5 rounded-full bg-surface-light text-text-muted">
              {{ playerStore.episodesQueue.length }}
            </span>
          </h4>
        </div>

        <!-- Scrollable episodes queue -->
        <div class="flex-1 overflow-y-auto space-y-2 pt-3 pr-1">
          <button
            v-for="ep in playerStore.episodesQueue"
            :key="ep.id"
            @click="selectEpisode(ep)"
            :class="[
              'w-full flex items-center gap-3 p-2.5 rounded-xl border text-left transition-all',
              ep.id === playerStore.currentEpisode?.id
                ? 'bg-primary/20 border-primary/40 shadow-glow-primary'
                : 'bg-surface/50 hover:bg-surface border-surface-border text-text-muted'
            ]"
          >
            <!-- Thumbnail -->
            <div class="relative w-16 aspect-video rounded-lg overflow-hidden bg-surface-light shrink-0">
              <img
                :src="ep.thumbnailUrl"
                :alt="ep.title"
                class="w-full h-full object-cover"
              />
              <div
                v-if="ep.id === playerStore.currentEpisode?.id"
                class="absolute inset-0 bg-primary/40 flex items-center justify-center text-white font-bold"
              >
                ▶
              </div>
            </div>

            <!-- Details -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-1.5">
                <span class="text-xs font-mono font-bold text-primary">
                  EP {{ ep.episodeNumber }}
                </span>
                <span v-if="ep.isFree" class="text-[9px] px-1 rounded bg-green-950 text-green-300 border border-green-700/30">
                  GRATIS
                </span>
              </div>
              <p :class="['text-xs font-semibold truncate', ep.id === playerStore.currentEpisode?.id ? 'text-white' : 'text-text-muted']">
                {{ ep.title }}
              </p>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Recommendations Catalog Section Below Player -->
    <div v-if="!playerStore.loading" class="max-w-7xl mx-auto w-full px-4 sm:px-6 mt-10 space-y-10">
      <!-- 1. Related Series / Similar Genre -->
      <section v-if="relatedSeries.length > 0" class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-5 bg-primary rounded-full"></span>
            <h3 class="text-lg sm:text-xl font-bold text-white">
              {{ currentLang === 'en' ? 'More Like This' : 'Series Similares Recomendadas' }}
            </h3>
          </div>
          <span class="text-xs text-text-muted font-medium">
            {{ currentLang === 'en' ? 'Binge-worthy picks' : 'Para seguir maratoneando' }}
          </span>
        </div>

        <div class="flex gap-4 overflow-x-auto pb-4 pt-1 no-scrollbar scroll-smooth">
          <div
            v-for="s in relatedSeries"
            :key="s.id"
            class="w-40 sm:w-48 flex-shrink-0"
          >
            <SeriesCard :series="s" />
          </div>
        </div>
      </section>

      <!-- 2. DramaVivo Exclusives -->
      <section v-if="sameSourceSeries.length > 0" class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-5 bg-secondary rounded-full"></span>
            <h3 class="text-lg sm:text-xl font-bold text-white">
              {{ currentLang === 'en' ? 'DramaVivo Exclusives' : 'Dramas Exclusivos DramaVivo' }}
            </h3>
          </div>
          <span class="text-xs text-text-muted font-medium">
            100% {{ currentLang === 'en' ? 'Free Episodes' : 'Gratis en HD' }}
          </span>
        </div>

        <div class="flex gap-4 overflow-x-auto pb-4 pt-1 no-scrollbar scroll-smooth">
          <div
            v-for="s in sameSourceSeries"
            :key="s.id"
            class="w-40 sm:w-48 flex-shrink-0"
          >
            <SeriesCard :series="s" />
          </div>
        </div>
      </section>

      <!-- 3. Top Trending in DramaVivo -->
      <section v-if="trendingSeries.length > 0" class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-1.5 h-5 bg-gradient-to-b from-primary to-secondary rounded-full"></span>
            <h3 class="text-lg sm:text-xl font-bold text-white">
              {{ currentLang === 'en' ? 'Top Trending on DramaVivo' : 'Tendencias Más Vistas en DramaVivo' }}
            </h3>
          </div>
          <span class="text-xs text-primary font-medium">
            🔥 {{ currentLang === 'en' ? 'Most Watched' : 'Lo Más Visto' }}
          </span>
        </div>

        <div class="flex gap-4 overflow-x-auto pb-4 pt-1 no-scrollbar scroll-smooth">
          <div
            v-for="s in trendingSeries"
            :key="s.id"
            class="w-40 sm:w-48 flex-shrink-0"
          >
            <SeriesCard :series="s" />
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
