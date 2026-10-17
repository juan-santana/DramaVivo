<script setup lang="ts">
import { onMounted, onUnmounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useHead } from '@unhead/vue'
import { useCatalogStore } from '../stores/catalog'
import { useFavoritesStore } from '../stores/favorites'
import { useI18n } from '../i18n'
import { seriesService } from '../services/series'
import SeriesGrid from '../components/catalog/SeriesGrid.vue'
import SeriesCard from '../components/catalog/SeriesCard.vue'
import GenreFilter from '../components/catalog/GenreFilter.vue'
import AdSlot from '../components/ads/AdSlot.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import type { Series, WatchHistoryItem } from '../types'

const router = useRouter()
const catalogStore = useCatalogStore()
const favoritesStore = useFavoritesStore()
const { t, currentLang } = useI18n()

// All series cache for rich curated collections
const allSeries = ref<Series[]>([])
const loadingAll = ref(true)

// NetShort 3D Cover Flow Hero State
const activeHeroIndex = ref(0)
let heroTimer: ReturnType<typeof setInterval> | null = null

// Horizontal Scroll Container Refs
const top10Container = ref<HTMLDivElement | null>(null)
const exclusivesContainer = ref<HTMLDivElement | null>(null)
const ceoContainer = ref<HTMLDivElement | null>(null)
const revengeContainer = ref<HTMLDivElement | null>(null)
const romanceContainer = ref<HTMLDivElement | null>(null)
const stardustContainer = ref<HTMLDivElement | null>(null)

useHead({
  title: 'DramaVivo - Microdramas y Series Cortas en Streaming HD',
  meta: [
    {
      name: 'description',
      content: 'Descubre los mejores microdramas en formato vertical 9:16. Romances, venganzas, multimillonarios y fantasía 100% gratis en DramaVivo.',
    },
    { property: 'og:title', content: 'DramaVivo - Series Cortas y Microdramas en Streaming' },
    {
      property: 'og:description',
      content: 'Plataforma líder de microdramas en streaming en español e inglés para ver desde cualquier dispositivo móvil.',
    },
    { property: 'og:type', content: 'website' },
  ],
})

// Top 8 Featured series for the NetShort 3D Carousel
const heroSeriesList = computed<Series[]>(() => {
  if (allSeries.value.length === 0) {
    return catalogStore.featured.length > 0 ? catalogStore.featured : []
  }
  // Curate 8 top quality series with real covers and videos
  return allSeries.value.filter(s => s.rating && s.rating >= 4.5).slice(0, 8)
})

// 3D Cover Flow Items: 5 visible cards centered around activeHeroIndex
const coverFlowCards = computed(() => {
  const list = heroSeriesList.value
  if (list.length === 0) return []
  const len = list.length
  
  return [-2, -1, 0, 1, 2].map(offset => {
    const idx = (activeHeroIndex.value + offset + len) % len
    return {
      offset,
      series: list[idx],
      index: idx
    }
  })
})

const currentHero = computed<Series | null>(() => {
  if (heroSeriesList.value.length === 0) return null
  return heroSeriesList.value[activeHeroIndex.value] || heroSeriesList.value[0] || null
})

const isHeroFavorite = computed(() => {
  return currentHero.value ? favoritesStore.isFavorite(currentHero.value.id) : false
})

// Top 10 by views
const top10Series = computed<Series[]>(() => {
  return [...allSeries.value]
    .sort((a, b) => (b.viewsCount || 0) - (a.viewsCount || 0))
    .slice(0, 10)
})

// Continue Watching List
const continueWatchingList = computed<WatchHistoryItem[]>(() => {
  return favoritesStore.history.slice(0, 8)
})

// Curated Thematic Rows (Cleaned of external platform names)
const dramaVivoExclusives = computed<Series[]>(() => {
  return allSeries.value.slice(0, 14)
})

const ceoSeries = computed<Series[]>(() => {
  return allSeries.value.filter(s =>
    s.genres.some(g => g.toLowerCase().includes('multimillonario')) ||
    s.title.toLowerCase().includes('ceo') ||
    s.title.toLowerCase().includes('multimillonario') ||
    s.title.toLowerCase().includes('jefe') ||
    s.title.toLowerCase().includes('heredero') ||
    (s.originalTitle && s.originalTitle.toLowerCase().includes('billionaire')) ||
    (s.originalTitle && s.originalTitle.toLowerCase().includes('ceo'))
  ).slice(0, 12)
})

const revengeSeries = computed<Series[]>(() => {
  return allSeries.value.filter(s =>
    s.genres.some(g => g.toLowerCase().includes('venganza')) ||
    s.title.toLowerCase().includes('venganza') ||
    s.title.toLowerCase().includes('ex') ||
    s.synopsis.toLowerCase().includes('venganza') ||
    (s.originalTitle && s.originalTitle.toLowerCase().includes('revenge'))
  ).slice(0, 12)
})

const romanceSeries = computed<Series[]>(() => {
  return allSeries.value.filter(s =>
    s.genres.some(g => g.toLowerCase().includes('romance') || g.toLowerCase().includes('pasión')) ||
    s.title.toLowerCase().includes('amor') ||
    s.title.toLowerCase().includes('esposa') ||
    s.title.toLowerCase().includes('boda')
  ).slice(0, 12)
})

const stardustSeries = computed<Series[]>(() => {
  return allSeries.value.filter(s =>
    s.id.startsWith('stardust-') ||
    s.id.startsWith('shorttv-') ||
    s.genres.some(g => g.toLowerCase().includes('stardust') || g.toLowerCase().includes('shorttv'))
  ).slice(0, 16)
})

function startHeroTimer() {
  stopHeroTimer()
  heroTimer = setInterval(() => {
    nextHero()
  }, 6000)
}

function stopHeroTimer() {
  if (heroTimer) {
    clearInterval(heroTimer)
    heroTimer = null
  }
}

function nextHero(manual = false) {
  if (heroSeriesList.value.length === 0) return
  activeHeroIndex.value = (activeHeroIndex.value + 1) % heroSeriesList.value.length
  if (manual) startHeroTimer()
}

function prevHero() {
  if (heroSeriesList.value.length === 0) return
  activeHeroIndex.value = (activeHeroIndex.value - 1 + heroSeriesList.value.length) % heroSeriesList.value.length
  startHeroTimer()
}

function selectHero(idx: number) {
  activeHeroIndex.value = idx
  startHeroTimer()
}

let touchStartX = 0
let touchStartY = 0
let touchEndX = 0
let touchEndY = 0
let isSwiping = false
let didSwipe = false

function handleTouchStart(e: TouchEvent) {
  if (e.touches.length !== 1) return
  touchStartX = e.touches[0].clientX
  touchStartY = e.touches[0].clientY
  touchEndX = touchStartX
  touchEndY = touchStartY
  isSwiping = true
  didSwipe = false
}

function handleTouchMove(e: TouchEvent) {
  if (!isSwiping || e.touches.length !== 1) return
  touchEndX = e.touches[0].clientX
  touchEndY = e.touches[0].clientY
}

function handleTouchEnd() {
  if (!isSwiping) return
  isSwiping = false

  const deltaX = touchEndX - touchStartX
  const deltaY = touchEndY - touchStartY

  // Trigger horizontal swipe if movement exceeds 35px and is predominantly horizontal
  if (Math.abs(deltaX) > 35 && Math.abs(deltaX) > Math.abs(deltaY) * 1.1) {
    didSwipe = true
    setTimeout(() => {
      didSwipe = false
    }, 200)

    if (deltaX < 0) {
      // Swiped Left -> advance to next drama
      nextHero(true)
    } else {
      // Swiped Right -> go to previous drama
      prevHero()
    }
  }
}

function onCardClick(item: { offset: number; series: Series; index: number }) {
  if (didSwipe) return
  if (item.offset === 0) {
    // Center card clicked -> go to player
    startWatching(item.series.id)
  } else {
    // Flanking card clicked -> rotate to center
    selectHero(item.index)
  }
}

function toggleHeroFavorite() {
  if (currentHero.value) {
    favoritesStore.toggleFavorite(currentHero.value)
  }
}

function startWatching(seriesId: string) {
  router.push(`/reproducir/${seriesId}`)
}

function resumeWatching(item: WatchHistoryItem) {
  router.push(`/reproducir/${item.seriesId}/${item.episodeId}`)
}

function getProgressPercentage(item: WatchHistoryItem): number {
  if (!item.durationSeconds || item.durationSeconds <= 0) return 0
  const pct = Math.round((item.progressSeconds / item.durationSeconds) * 100)
  return Math.min(Math.max(pct, 5), 100)
}

function onGenreSelect(genreName: string) {
  router.push(`/catalogo?genre=${encodeURIComponent(genreName)}`)
}

function scrollRow(el: HTMLDivElement | null, direction: 'left' | 'right') {
  if (!el) return
  const offset = direction === 'left' ? -420 : 420
  el.scrollBy({ left: offset, behavior: 'smooth' })
}

onMounted(async () => {
  catalogStore.fetchHomeData()
  try {
    const res = await seriesService.getAll({ pageSize: 120 })
    allSeries.value = res.data
  } catch (err) {
    console.error('Error fetching all series:', err)
  } finally {
    loadingAll.value = false
  }
  startHeroTimer()
})

onUnmounted(() => {
  stopHeroTimer()
})
</script>

<template>
  <div class="space-y-12 pb-24 overflow-x-hidden">
    <!-- Initial Loading State -->
    <div v-if="loadingAll && !currentHero" class="min-h-[75vh] flex items-center justify-center">
      <LoadingSpinner size="lg" text="Preparando la experiencia cinematográfica de DramaVivo..." />
    </div>

    <template v-else>
      <!-- ======================================================= -->
      <!-- 1. NetShort-Style 3D Cover Flow Cinema Hero Carousel   -->
      <!-- ======================================================= -->
      <section
        v-if="currentHero"
        class="relative w-full pt-6 pb-12 overflow-hidden bg-gradient-to-b from-[#0a0a14] via-[#08080f] to-background"
      >
        <!-- Ambient Theater Curtains (Deep Red/Burgundy edges inspired by NetShort) -->
        <div class="absolute inset-y-0 left-0 w-32 sm:w-64 bg-gradient-to-r from-red-950/40 via-red-900/10 to-transparent pointer-events-none z-10"></div>
        <div class="absolute inset-y-0 right-0 w-32 sm:w-64 bg-gradient-to-l from-red-950/40 via-red-900/10 to-transparent pointer-events-none z-10"></div>

        <!-- Ambient Overhead Cinema Spotlight -->
        <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[350px] bg-gradient-to-b from-amber-400/15 via-white/5 to-transparent rounded-full blur-3xl pointer-events-none"></div>

        <!-- Left & Right Arrow Navigation Buttons (Desktop only: hidden on mobile) -->
        <button
          @click="prevHero"
          class="hidden md:flex absolute left-4 sm:left-8 top-1/2 -translate-y-1/2 z-40 w-11 h-11 sm:w-13 sm:h-13 rounded-full bg-black/60 hover:bg-black/90 border border-white/20 text-white items-center justify-center backdrop-blur-md transition-all hover:scale-110 shadow-2xl"
          aria-label="Anterior drama"
        >
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <button
          @click="nextHero(true)"
          class="hidden md:flex absolute right-4 sm:right-8 top-1/2 -translate-y-1/2 z-40 w-11 h-11 sm:w-13 sm:h-13 rounded-full bg-black/60 hover:bg-black/90 border border-white/20 text-white items-center justify-center backdrop-blur-md transition-all hover:scale-110 shadow-2xl"
          aria-label="Siguiente drama"
        >
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
          </svg>
        </button>

        <!-- 3D Cover Flow Stage with Mobile Swipe Support -->
        <div
          class="relative max-w-7xl mx-auto px-4 sm:px-6 h-[460px] sm:h-[520px] flex items-center justify-center touch-pan-y cursor-grab active:cursor-grabbing"
          @touchstart="handleTouchStart"
          @touchmove="handleTouchMove"
          @touchend="handleTouchEnd"
        >
          <div class="relative w-full h-full flex items-center justify-center perspective-[1200px]">
            <!-- Render the 5 Visible 3D Cards -->
            <div
              v-for="item in coverFlowCards"
              :key="item.series.id + '-' + item.offset"
              @click="onCardClick(item)"
              :class="[
                'absolute transition-all duration-500 ease-out select-none flex flex-col items-center',
                // Center active card
                item.offset === 0 && 'z-30 scale-105 sm:scale-115 opacity-100 cursor-pointer',
                // Left 1 card
                item.offset === -1 && 'z-20 scale-90 opacity-70 brightness-75 -translate-x-36 sm:-translate-x-64 lg:-translate-x-80 cursor-pointer',
                // Right 1 card
                item.offset === 1 && 'z-20 scale-90 opacity-70 brightness-75 translate-x-36 sm:translate-x-64 lg:translate-x-80 cursor-pointer',
                // Far Left 2 card
                item.offset === -2 && 'z-10 scale-75 opacity-35 brightness-50 -translate-x-64 sm:-translate-x-[420px] lg:-translate-x-[520px] hidden md:flex cursor-pointer',
                // Far Right 2 card
                item.offset === 2 && 'z-10 scale-75 opacity-35 brightness-50 translate-x-64 sm:translate-x-[420px] lg:translate-x-[520px] hidden md:flex cursor-pointer'
              ]"
            >
              <!-- Poster Frame with NetShort Glow -->
              <div
                :class="[
                  'relative w-44 sm:w-56 md:w-64 aspect-[2/3] rounded-2xl overflow-hidden bg-surface-dark border transition-all duration-300',
                  item.offset === 0
                    ? 'border-amber-400/80 shadow-[0_15px_50px_rgba(245,197,24,0.35)] ring-2 ring-amber-400/40'
                    : 'border-white/10 shadow-2xl hover:border-white/30'
                ]"
              >
                <img
                  :src="item.series.verticalPosterUrl || item.series.posterUrl"
                  :alt="item.series.title"
                  class="w-full h-full object-cover"
                />

                <!-- NetShort Style 'EXCLUSIVE' Ribbon -->
                <div class="absolute top-2.5 left-2.5 z-10 flex items-center gap-1 px-2 py-0.5 rounded-md bg-black/70 backdrop-blur-md border border-white/20 text-[10px] font-bold text-amber-400 uppercase tracking-wider">
                  <span>★</span> EXCLUSIVO
                </div>

                <!-- Dark gradient bottom -->
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>

                <!-- Rating badge bottom right -->
                <div class="absolute bottom-2.5 right-2.5 flex items-center gap-1 text-[11px] font-bold text-secondary bg-black/70 backdrop-blur-md px-2 py-0.5 rounded-md border border-secondary/30">
                  <svg class="w-3 h-3 fill-current" viewBox="0 0 24 24">
                    <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
                  </svg>
                  <span>{{ item.series.rating || '9.6' }}</span>
                </div>
              </div>

              <!-- Title beneath cards (NetShort style) -->
              <div
                :class="[
                  'mt-3 text-center transition-all duration-300 max-w-[240px]',
                  item.offset === 0 ? 'opacity-100 scale-100' : 'opacity-60 scale-90'
                ]"
              >
                <p class="text-xs sm:text-sm font-black text-white truncate drop-shadow-md">
                  {{ currentLang === 'en' && item.series.originalTitle ? item.series.originalTitle : item.series.title }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Cinema Floor Arc & Dot Indicators (Inspired by NetShort curved bar) -->
        <div class="relative max-w-xl mx-auto px-4 mt-2 flex flex-col items-center">
          <!-- Curved floor glowing arc line -->
          <div class="w-full h-3 rounded-[100%] border-t border-white/20 shadow-[0_-4px_15px_rgba(255,255,255,0.15)] flex items-center justify-center"></div>

          <!-- Dot Indicators with 6s Progress Bar -->
          <div class="flex items-center gap-2.5 -mt-1.5">
            <button
              v-for="(hero, idx) in heroSeriesList"
              :key="hero.id"
              @click="selectHero(idx)"
              class="relative rounded-full overflow-hidden transition-all duration-300 focus:outline-none"
              :class="[
                idx === activeHeroIndex
                  ? 'w-10 h-2 bg-white/20 ring-1 ring-amber-400/60 shadow-glow-secondary'
                  : 'w-2.5 h-2.5 bg-white/30 hover:bg-white/60'
              ]"
              :aria-label="`Ir a drama ${idx + 1}`"
            >
              <span
                v-if="idx === activeHeroIndex"
                :key="`hero-progress-${activeHeroIndex}`"
                class="absolute inset-0 bg-gradient-to-r from-amber-400 via-rose-500 to-orange-500 rounded-full animate-progress-6s"
              ></span>
            </button>
          </div>
        </div>

        <!-- Center Active Drama Details & Action Buttons -->
        <div class="max-w-3xl mx-auto px-4 text-center mt-6 space-y-3.5">
          <!-- Badges -->
          <div class="flex flex-wrap items-center justify-center gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-primary text-white uppercase tracking-wider shadow-glow-primary">
              100% GRATIS • SIN MONEDAS
            </span>
            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-surface-light border border-surface-border text-text-muted">
              {{ currentHero.totalEpisodes === 1 ? (currentLang === 'en' ? 'Movie 1h+' : 'Película 1h+') : `${currentHero.totalEpisodes} ${t('hero.episodesCount')}` }}
            </span>
            <span
              v-for="g in currentHero.genres.slice(0, 3)"
              :key="g"
              class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-white/10 text-white/90 border border-white/10"
            >
              {{ g }}
            </span>
          </div>

          <!-- Synopsis Preview -->
          <p class="text-xs sm:text-sm text-text-muted/90 line-clamp-2 leading-relaxed max-w-2xl mx-auto">
            {{ currentHero.synopsis }}
          </p>

          <!-- Action Buttons -->
          <div class="flex flex-wrap items-center justify-center gap-3 pt-1">
            <button
              @click="startWatching(currentHero.id)"
              class="px-7 py-3 rounded-xl bg-gradient-to-r from-rose-600 via-primary to-orange-500 hover:from-rose-500 hover:to-orange-400 text-white font-bold text-sm shadow-glow-primary hover:scale-105 transition-all flex items-center gap-2"
            >
              <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
              <span>{{ t('hero.watchNow') }}</span>
            </button>

            <button
              @click="toggleHeroFavorite"
              :class="[
                'px-5 py-3 rounded-xl font-bold text-sm backdrop-blur-md border transition-all flex items-center gap-2',
                isHeroFavorite
                  ? 'bg-secondary/20 border-secondary text-secondary shadow-glow-secondary'
                  : 'bg-surface/80 hover:bg-surface border-white/20 text-white'
              ]"
            >
              <svg class="w-4 h-4" :fill="isHeroFavorite ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              <span>{{ isHeroFavorite ? 'Favorito' : 'Mi lista' }}</span>
            </button>

            <router-link
              :to="`/serie/${currentHero.slug || currentHero.id}`"
              class="px-4 py-3 rounded-xl bg-surface-light/60 hover:bg-surface-light border border-surface-border text-text-muted hover:text-white text-sm font-semibold transition-colors"
            >
              {{ t('series.details') }}
            </router-link>
          </div>
        </div>
      </section>

      <!-- Main Container for Rows & Catalogs -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <!-- ========================================== -->
        <!-- 2. Continuar Viendo (Watch History)        -->
        <!-- ========================================== -->
        <section v-if="continueWatchingList.length > 0" class="space-y-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-1.5 h-5 bg-primary rounded-full"></span>
              <h2 class="text-xl sm:text-2xl font-black text-white">
                {{ t('home.continueWatching') }}
              </h2>
            </div>
            <button
              @click="favoritesStore.clearHistory"
              class="text-xs text-text-muted hover:text-white transition-colors font-medium"
            >
              Limpiar historial
            </button>
          </div>

          <div class="flex items-stretch gap-4 overflow-x-auto no-scrollbar py-2 -mx-4 px-4 sm:mx-0 sm:px-0">
            <div
              v-for="item in continueWatchingList"
              :key="item.seriesId"
              @click="resumeWatching(item)"
              class="w-60 sm:w-68 shrink-0 group bg-surface rounded-2xl border border-surface-border overflow-hidden cursor-pointer hover:border-primary/50 transition-all card-hover-glow"
            >
              <div class="relative aspect-video w-full bg-surface-light overflow-hidden">
                <img
                  :src="item.posterUrl"
                  :alt="item.seriesTitle"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div class="absolute inset-0 bg-black/40 group-hover:bg-black/20 transition-colors flex items-center justify-center">
                  <div class="w-10 h-10 rounded-full bg-primary/90 text-white flex items-center justify-center shadow-glow-primary transform group-hover:scale-110 transition-transform">
                    <svg class="w-5 h-5 fill-current translate-x-0.5" viewBox="0 0 24 24">
                      <path d="M8 5v14l11-7z" />
                    </svg>
                  </div>
                </div>

                <!-- Progress Bar at bottom of card thumbnail -->
                <div class="absolute bottom-0 inset-x-0 h-1.5 bg-black/60">
                  <div
                    class="h-full bg-primary"
                    :style="{ width: `${getProgressPercentage(item)}%` }"
                  ></div>
                </div>
              </div>

              <div class="p-3 space-y-1">
                <div class="flex items-center justify-between text-xs">
                  <span class="font-bold text-primary font-mono">
                    {{ t('home.ep') }} {{ item.episodeNumber }}
                  </span>
                  <span class="text-[11px] text-text-muted">
                    {{ getProgressPercentage(item) }}% visto
                  </span>
                </div>
                <h4 class="text-xs sm:text-sm font-bold text-white truncate group-hover:text-primary transition-colors">
                  {{ item.seriesTitle }}
                </h4>
              </div>
            </div>
          </div>
        </section>

        <!-- ========================================== -->
        <!-- 3. Top 10 en DramaVivo Hoy (Giant Numbers)-->
        <!-- ========================================== -->
        <section class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl sm:text-2xl font-black text-white flex items-center gap-2">
                <span class="text-secondary font-mono font-bold text-lg bg-secondary/20 px-2 py-0.5 rounded-md border border-secondary/30">TOP</span>
                <span>{{ t('home.top10') }}</span>
              </h2>
              <p class="text-xs text-text-muted">Los microdramas más vistos en streaming HD</p>
            </div>

            <!-- Scroll arrows -->
            <div class="hidden sm:flex items-center gap-2">
              <button
                @click="scrollRow(top10Container, 'left')"
                class="p-2 rounded-xl bg-surface hover:bg-surface-light border border-surface-border text-text-muted hover:text-white transition-colors"
                aria-label="Izquierda"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                @click="scrollRow(top10Container, 'right')"
                class="p-2 rounded-xl bg-surface hover:bg-surface-light border border-surface-border text-text-muted hover:text-white transition-colors"
                aria-label="Derecha"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          <div
            ref="top10Container"
            class="flex items-end gap-3 sm:gap-6 overflow-x-auto no-scrollbar py-4 -mx-4 px-4 sm:mx-0 sm:px-0"
          >
            <div
              v-for="(s, index) in top10Series"
              :key="s.id"
              class="relative flex items-center shrink-0 group cursor-pointer"
            >
              <!-- Giant Outline Rank Number (Netflix style) -->
              <span class="stroke-number text-7xl sm:text-9xl font-black italic select-none -mr-4 sm:-mr-7 z-0 pointer-events-none transform -translate-y-2">
                {{ index + 1 }}
              </span>

              <!-- Poster Card -->
              <div class="w-36 sm:w-44 z-10">
                <SeriesCard :series="s" aspectRatio="2/3" />
              </div>
            </div>
          </div>
        </section>

        <!-- ========================================== -->
        <!-- 4. Dramas Exclusivos DramaVivo             -->
        <!-- ========================================== -->
        <section class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl sm:text-2xl font-black text-white flex items-center gap-2">
                <span class="text-amber-400">★</span>
                <span>{{ t('home.exclusive') }}</span>
              </h2>
              <p class="text-xs text-text-muted">Producciones originales completas en formato vertical 9:16</p>
            </div>

            <div class="flex items-center gap-2">
              <button
                @click="scrollRow(exclusivesContainer, 'left')"
                class="p-2 rounded-xl bg-surface hover:bg-surface-light border border-surface-border text-text-muted hover:text-white transition-colors"
                aria-label="Izquierda"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                @click="scrollRow(exclusivesContainer, 'right')"
                class="p-2 rounded-xl bg-surface hover:bg-surface-light border border-surface-border text-text-muted hover:text-white transition-colors"
                aria-label="Derecha"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          <div
            ref="exclusivesContainer"
            class="flex items-stretch gap-4 overflow-x-auto no-scrollbar py-2 -mx-4 px-4 sm:mx-0 sm:px-0"
          >
            <div
              v-for="s in dramaVivoExclusives"
              :key="s.id"
              class="w-40 sm:w-48 shrink-0"
            >
              <SeriesCard :series="s" aspectRatio="2/3" />
            </div>
          </div>
        </section>

        <!-- ========================================== -->
        <!-- 5. Curated Thematic Row: CEOs y Millonarios-->
        <!-- ========================================== -->
        <section v-if="ceoSeries.length > 0" class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl sm:text-2xl font-black text-white flex items-center gap-2">
                <span>{{ t('home.ceos') }}</span>
              </h2>
              <p class="text-xs text-text-muted">Amores por contrato, herederos secretos y poder supremo</p>
            </div>

            <div class="flex items-center gap-2">
              <button
                @click="scrollRow(ceoContainer, 'left')"
                class="p-2 rounded-xl bg-surface hover:bg-surface-light border border-surface-border text-text-muted hover:text-white transition-colors"
                aria-label="Izquierda"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                @click="scrollRow(ceoContainer, 'right')"
                class="p-2 rounded-xl bg-surface hover:bg-surface-light border border-surface-border text-text-muted hover:text-white transition-colors"
                aria-label="Derecha"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          <div
            ref="ceoContainer"
            class="flex items-stretch gap-4 overflow-x-auto no-scrollbar py-2 -mx-4 px-4 sm:mx-0 sm:px-0"
          >
            <div
              v-for="s in ceoSeries"
              :key="s.id"
              class="w-40 sm:w-48 shrink-0"
            >
              <SeriesCard :series="s" aspectRatio="2/3" />
            </div>
          </div>
        </section>

        <!-- Sponsored Ad Slot -->
        <AdSlot />

        <!-- ========================================== -->
        <!-- 6. Curated Thematic Row: Venganzas         -->
        <!-- ========================================== -->
        <section v-if="revengeSeries.length > 0" class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl sm:text-2xl font-black text-white flex items-center gap-2">
                <span>{{ t('home.revenge') }}</span>
              </h2>
              <p class="text-xs text-text-muted">Traiciones imperdonables y el dulce sabor de la revancha</p>
            </div>

            <div class="flex items-center gap-2">
              <button
                @click="scrollRow(revengeContainer, 'left')"
                class="p-2 rounded-xl bg-surface hover:bg-surface-light border border-surface-border text-text-muted hover:text-white transition-colors"
                aria-label="Izquierda"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                @click="scrollRow(revengeContainer, 'right')"
                class="p-2 rounded-xl bg-surface hover:bg-surface-light border border-surface-border text-text-muted hover:text-white transition-colors"
                aria-label="Derecha"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          <div
            ref="revengeContainer"
            class="flex items-stretch gap-4 overflow-x-auto no-scrollbar py-2 -mx-4 px-4 sm:mx-0 sm:px-0"
          >
            <div
              v-for="s in revengeSeries"
              :key="s.id"
              class="w-40 sm:w-48 shrink-0"
            >
              <SeriesCard :series="s" aspectRatio="2/3" />
            </div>
          </div>
        </section>

        <!-- ========================================== -->
        <!-- 7. Estrenos StardustTV & ShortTV           -->
        <!-- ========================================== -->
        <section v-if="stardustSeries.length > 0" class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl sm:text-2xl font-black text-white flex items-center gap-2">
                <span>{{ t('home.stardustShorts') }}</span>
              </h2>
              <p class="text-xs text-text-muted">Nuevos microdramas verticales en español e inglés recién incorporados</p>
            </div>

            <div class="flex items-center gap-2">
              <button
                @click="scrollRow(stardustContainer, 'left')"
                class="p-2 rounded-xl bg-surface hover:bg-surface-light border border-surface-border text-text-muted hover:text-white transition-colors"
                aria-label="Izquierda"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                @click="scrollRow(stardustContainer, 'right')"
                class="p-2 rounded-xl bg-surface hover:bg-surface-light border border-surface-border text-text-muted hover:text-white transition-colors"
                aria-label="Derecha"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          <div
            ref="stardustContainer"
            class="flex items-stretch gap-4 overflow-x-auto no-scrollbar py-2 -mx-4 px-4 sm:mx-0 sm:px-0"
          >
            <div
              v-for="s in stardustSeries"
              :key="s.id"
              class="w-44 sm:w-56 shrink-0"
            >
              <SeriesCard :series="s" aspectRatio="2/3" />
            </div>
          </div>
        </section>

        <!-- ========================================== -->
        <!-- 8. Genre Explorer Bar                      -->
        <!-- ========================================== -->
        <section class="space-y-3">
          <div class="flex items-center justify-between">
            <h2 class="text-base sm:text-lg font-bold text-white tracking-wide">
              {{ t('home.exploreGenres') }}
            </h2>
            <router-link to="/catalogo" class="text-xs font-semibold text-primary hover:underline">
              {{ t('home.viewAll') }} →
            </router-link>
          </div>
          <GenreFilter
            :genres="catalogStore.genres"
            selectedGenre=""
            @select="onGenreSelect"
          />
        </section>

        <!-- ========================================== -->
        <!-- 9. Recién Agregados (Grid Completo)        -->
        <!-- ========================================== -->
        <section class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl sm:text-2xl font-black text-white flex items-center gap-2">
                <span class="text-secondary">✨</span> {{ t('hero.recentlyAdded') }}
              </h2>
              <p class="text-xs text-text-muted">Nuevos episodios incorporados diariamente</p>
            </div>
            <router-link to="/catalogo?sort=recent" class="text-xs font-semibold text-primary hover:underline">
              {{ t('hero.exploreCatalog') }} →
            </router-link>
          </div>

          <SeriesGrid :series="catalogStore.recent" :loading="catalogStore.loadingHome" />
        </section>

        <!-- ========================================== -->
        <!-- 10. Editorial VIP Banner                   -->
        <!-- ========================================== -->
        <section class="rounded-3xl overflow-hidden glass-panel border border-surface-border p-6 sm:p-10 relative">
          <div class="max-w-xl space-y-3 relative z-10">
            <span class="text-xs font-bold text-secondary uppercase tracking-widest flex items-center gap-1.5">
              <span>⭐</span> {{ t('hero.editorialPicks') }} DramaVivo
            </span>
            <h3 class="text-2xl sm:text-3xl font-black text-white leading-tight">
              Sin monedas. Sin recargas. Todos los episodios libres.
            </h3>
            <p class="text-xs sm:text-sm text-text-muted leading-relaxed">
              Disfruta del catálogo completo de más de 90 microdramas exclusivos en alta definición y con subtítulos cinematográficos sincronizados.
            </p>
            <div class="pt-2 flex flex-wrap gap-3">
              <router-link
                to="/catalogo"
                class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white text-black font-bold text-xs hover:bg-neutral-200 transition-all shadow-lg"
              >
                <span>{{ t('hero.exploreCatalog') }}</span>
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </router-link>
            </div>
          </div>

          <div class="absolute -right-12 -bottom-12 w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none"></div>
        </section>
      </div>
    </template>
  </div>
</template>

<style scoped>
@keyframes progress6s {
  0% {
    width: 0%;
  }
  100% {
    width: 100%;
  }
}

.animate-progress-6s {
  animation: progress6s 6s linear forwards;
}
</style>
