<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHead } from '@unhead/vue'
import type { Series, Episode } from '../types'
import { seriesService } from '../services/series'
import { useFavoritesStore } from '../stores/favorites'
import { useI18n } from '../i18n'
import EpisodeList from '../components/catalog/EpisodeList.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import AdSlot from '../components/ads/AdSlot.vue'

const route = useRoute()
const router = useRouter()
const favoritesStore = useFavoritesStore()
const { t, currentLang } = useI18n()

const series = ref<Series | null>(null)
const episodes = ref<Episode[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const isFav = computed(() => {
  return series.value ? favoritesStore.isFavorite(series.value.id) : false
})

const lastWatched = computed(() => {
  return series.value ? favoritesStore.getHistoryItem(series.value.id) : undefined
})

const actionButtonLabel = computed(() => {
  if (lastWatched.value) {
    return `${t('series.continueWatching')} (Ep. ${lastWatched.value.episodeNumber})`
  }
  return t('series.startWatching')
})

useHead({
  title: computed(() => (series.value ? `${series.value.title} - DramaApp` : 'Cargando Serie...')),
  meta: [
    {
      name: 'description',
      content: computed(() => series.value?.synopsis || 'Ver microdrama en streaming vertical.'),
    },
    {
      property: 'og:title',
      content: computed(() => series.value?.title || 'DramaApp'),
    },
    {
      property: 'og:image',
      content: computed(() => series.value?.posterUrl || ''),
    },
  ],
})

async function loadData() {
  const idOrSlug = route.params.id as string
  loading.value = true
  error.value = null
  try {
    const s = await seriesService.getById(idOrSlug)
    series.value = s
    const epList = await seriesService.getEpisodes(s.id)
    episodes.value = epList
  } catch (err: unknown) {
    error.value = err instanceof Error ? err.message : 'No se pudo cargar la serie.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})

watch(
  () => route.params.id,
  () => {
    loadData()
  }
)

function toggleFavorite() {
  if (series.value) {
    favoritesStore.toggleFavorite(series.value)
  }
}

function playEpisode(ep: Episode) {
  if (!series.value) return
  router.push(`/reproducir/${series.value.id}/${ep.id}`)
}

function handleMainAction() {
  if (!series.value) return
  if (lastWatched.value) {
    router.push(`/reproducir/${series.value.id}/${lastWatched.value.episodeId}`)
  } else if (episodes.value.length > 0) {
    router.push(`/reproducir/${series.value.id}/${episodes.value[0].id}`)
  }
}
</script>

<template>
  <div class="relative min-h-screen pb-16">
    <!-- Loading state -->
    <div v-if="loading" class="min-h-[70vh] flex items-center justify-center">
      <LoadingSpinner size="lg" text="Cargando detalles del drama..." />
    </div>

    <!-- Error state -->
    <div v-else-if="error || !series" class="min-h-[50vh] flex flex-col items-center justify-center text-center p-4">
      <h2 class="text-2xl font-bold text-white mb-2">Serie no encontrada</h2>
      <p class="text-sm text-text-muted mb-6">{{ error || 'El título solicitado no existe o fue retirado.' }}</p>
      <router-link
        to="/catalogo"
        class="px-5 py-2.5 rounded-xl bg-primary text-white font-semibold text-xs shadow-glow-primary"
      >
        Explorar catálogo
      </router-link>
    </div>

    <!-- Series Content -->
    <div v-else class="space-y-8">
      <!-- Full Poster Blurred Background Hero -->
      <div class="relative w-full overflow-hidden bg-background">
        <!-- Background Blur Image -->
        <div class="absolute inset-0 overflow-hidden pointer-events-none">
          <img
            :src="series.bannerUrl || series.posterUrl"
            :alt="series.title"
            class="w-full h-full object-cover filter blur-3xl opacity-30 scale-125 transform"
          />
          <div class="absolute inset-0 bg-gradient-to-b from-background/40 via-background/80 to-background"></div>
        </div>

        <!-- Hero Content Section -->
        <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 sm:pt-14 pb-10">
          <div class="flex flex-col md:flex-row items-center md:items-start gap-8 lg:gap-12">
            <!-- Poster Card -->
            <div class="w-56 sm:w-64 lg:w-72 shrink-0 aspect-[2/3] rounded-2xl overflow-hidden shadow-2xl border border-surface-border bg-surface relative group">
              <img
                :src="series.posterUrl"
                :alt="series.title"
                class="w-full h-full object-cover"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end p-4">
                <span class="text-xs font-semibold text-white/90">
                  {{ series.totalEpisodes }} episodios completos
                </span>
              </div>
            </div>

            <!-- Details metadata -->
            <div class="flex-1 text-center md:text-left space-y-4">
              <!-- Badges row -->
              <div class="flex flex-wrap items-center justify-center md:justify-start gap-2.5">
                <span class="px-2.5 py-0.5 rounded-md bg-primary text-white text-xs font-black uppercase tracking-wider">
                  {{ series.status === 'completed' ? 'Completa' : 'En Emisión' }}
                </span>
                <span v-if="series.releaseYear" class="px-2 py-0.5 rounded-md bg-surface-light border border-surface-border text-xs text-text-muted">
                  {{ series.releaseYear }}
                </span>
                <span class="flex items-center gap-1 text-xs font-bold text-secondary bg-black/60 px-2 py-0.5 rounded-md border border-secondary/30">
                  ★ {{ series.rating?.toFixed(1) || '4.8' }}
                </span>
                <span v-if="series.viewsCount" class="text-xs text-text-muted">
                  {{ (series.viewsCount).toLocaleString('es-ES') }} visualizaciones
                </span>
              </div>

              <!-- Title -->
              <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight leading-tight">
                {{ currentLang === 'en' && series.originalTitle ? series.originalTitle : series.title }}
              </h1>
              <p v-if="series.originalTitle && series.originalTitle !== series.title" class="text-xs font-mono text-text-muted">
                {{ currentLang === 'en' ? `Original title: ${series.title}` : `Título en inglés: ${series.originalTitle}` }}
              </p>

              <!-- Genres chips -->
              <div class="flex flex-wrap items-center justify-center md:justify-start gap-2 pt-1">
                <router-link
                  v-for="genre in series.genres"
                  :key="genre"
                  :to="`/catalogo?genre=${encodeURIComponent(genre)}`"
                  class="px-3 py-1 rounded-full text-xs font-semibold bg-surface-light hover:bg-surface-lighter text-white/90 border border-surface-border transition-colors"
                >
                  {{ genre }}
                </router-link>
              </div>

              <!-- Synopsis -->
              <p class="text-sm sm:text-base text-text-muted leading-relaxed max-w-3xl pt-2">
                {{ series.synopsis }}
              </p>

              <!-- Action Buttons -->
              <div class="flex flex-wrap items-center justify-center md:justify-start gap-3 pt-4">
                <button
                  @click="handleMainAction"
                  class="px-6 py-3.5 rounded-xl bg-primary hover:bg-primary-hover text-white font-bold text-sm shadow-glow-primary hover:scale-105 transition-all flex items-center gap-2"
                >
                  <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                  <span>{{ actionButtonLabel }}</span>
                </button>

                <button
                  @click="toggleFavorite"
                  :class="[
                    'px-5 py-3.5 rounded-xl font-semibold text-sm border backdrop-blur-md transition-all flex items-center gap-2',
                    isFav
                      ? 'bg-secondary/20 border-secondary text-secondary shadow-glow-gold'
                      : 'bg-surface hover:bg-surface-light border-surface-border text-white'
                  ]"
                >
                  <svg class="w-5 h-5" :fill="isFav ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0z" />
                  </svg>
                  <span>{{ isFav ? (currentLang === 'en' ? '✓ In My List' : '✓ En Mi Lista') : (currentLang === 'en' ? '+ Add to My List' : '+ Mi Lista') }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Container for Episodes & Details -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
        <!-- Episodes Section -->
        <section class="glass-panel p-6 sm:p-8 rounded-3xl border border-surface-border">
          <EpisodeList
            :episodes="episodes"
            :currentEpisodeId="lastWatched?.episodeId"
            @select="playEpisode"
          />
        </section>

        <!-- Rights and Legal clearance notice -->
        <div class="p-4 rounded-2xl bg-surface/40 border border-surface-border text-xs text-text-muted flex items-start gap-3">
          <svg class="w-5 h-5 text-secondary shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          <div>
            <p class="font-semibold text-white">Contenido Licenciado Oficialmente</p>
            <p class="mt-0.5 text-text-dim leading-relaxed">
              Esta obra audiovisual se distribuye con autorización conforme a las leyes de propiedad intelectual internacionales para territorio de habla hispana. Si consideras que se ha cometido alguna infracción, puedes remitir una solicitud en nuestra sección legal.
            </p>
          </div>
        </div>

        <!-- Ad slot -->
        <AdSlot />
      </div>
    </div>
  </div>
</template>
