import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Series, Episode } from '../types'
import { seriesService } from '../services/series'
import { useFavoritesStore } from './favorites'

export const usePlayerStore = defineStore('player', () => {
  const currentSeries = ref<Series | null>(null)
  const currentEpisode = ref<Episode | null>(null)
  const episodesQueue = ref<Episode[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const currentTime = ref(0)
  const duration = ref(0)
  const isPlaying = ref(false)
  const isMuted = ref(false)
  const volume = ref(1)

  const currentIndex = computed(() => {
    if (!currentEpisode.value) return -1
    return episodesQueue.value.findIndex(e => e.id === currentEpisode.value?.id)
  })

  const hasNext = computed(() => {
    if (currentIndex.value === -1) return false
    return currentIndex.value < episodesQueue.value.length - 1
  })

  const hasPrev = computed(() => {
    return currentIndex.value > 0
  })

  const nextEpisode = computed<Episode | null>(() => {
    if (!hasNext.value) return null
    return episodesQueue.value[currentIndex.value + 1] || null
  })

  const prevEpisode = computed<Episode | null>(() => {
    if (!hasPrev.value) return null
    return episodesQueue.value[currentIndex.value - 1] || null
  })

  async function loadEpisode(seriesId: string, episodeId?: string) {
    loading.value = true
    error.value = null
    try {
      // 1. Load series info
      const s = await seriesService.getById(seriesId)
      currentSeries.value = s

      // 2. Load episodes list
      const eps = await seriesService.getEpisodes(s.id)
      episodesQueue.value = eps

      // 3. Select target episode
      let targetEp: Episode | undefined
      if (episodeId) {
        targetEp = eps.find(e => e.id === episodeId || String(e.episodeNumber) === String(episodeId))
      }
      if (!targetEp && eps.length > 0) {
        targetEp = eps[0]
      }

      currentEpisode.value = targetEp || null

      // Check saved progress from favorites/history store
      if (currentEpisode.value && currentSeries.value) {
        const favStore = useFavoritesStore()
        const historyItem = favStore.getHistoryItem(currentSeries.value.id)
        if (historyItem && historyItem.episodeId === currentEpisode.value.id) {
          currentTime.value = historyItem.progressSeconds
        } else {
          currentTime.value = 0
        }
      }
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al cargar el reproductor'
    } finally {
      loading.value = false
    }
  }

  function updateProgress(progressSec: number, totalDurationSec?: number) {
    currentTime.value = progressSec
    if (totalDurationSec) {
      duration.value = totalDurationSec
    }

    if (currentSeries.value && currentEpisode.value && progressSec > 3) {
      const favStore = useFavoritesStore()
      favStore.saveWatchHistory({
        seriesId: currentSeries.value.id,
        episodeId: currentEpisode.value.id,
        episodeNumber: currentEpisode.value.episodeNumber,
        seriesTitle: currentSeries.value.title,
        posterUrl: currentSeries.value.posterUrl,
        progressSeconds: Math.floor(progressSec),
        durationSeconds: Math.floor(totalDurationSec || currentEpisode.value.duration || 120),
        lastWatchedAt: new Date().toISOString(),
      })
    }
  }

  return {
    currentSeries,
    currentEpisode,
    episodesQueue,
    loading,
    error,
    currentTime,
    duration,
    isPlaying,
    isMuted,
    volume,
    currentIndex,
    hasNext,
    hasPrev,
    nextEpisode,
    prevEpisode,
    loadEpisode,
    updateProgress,
  }
})
