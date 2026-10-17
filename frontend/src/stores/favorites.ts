import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { FavoriteItem, WatchHistoryItem, Series } from '../types'

const FAVORITES_KEY = 'dramaapp_favorites'
const HISTORY_KEY = 'dramaapp_watch_history'

export const useFavoritesStore = defineStore('favorites', () => {
  const favorites = ref<FavoriteItem[]>(
    (() => {
      try {
        const stored = localStorage.getItem(FAVORITES_KEY)
        return stored ? JSON.parse(stored) : []
      } catch {
        return []
      }
    })()
  )

  const history = ref<WatchHistoryItem[]>(
    (() => {
      try {
        const stored = localStorage.getItem(HISTORY_KEY)
        return stored ? JSON.parse(stored) : []
      } catch {
        return []
      }
    })()
  )

  function saveToStorage() {
    try {
      localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites.value))
      localStorage.setItem(HISTORY_KEY, JSON.stringify(history.value))
    } catch {
      // Ignore storage quota exceeded
    }
  }

  function isFavorite(seriesId: string): boolean {
    return favorites.value.some(f => f.seriesId === seriesId)
  }

  function toggleFavorite(series: Series) {
    const idx = favorites.value.findIndex(f => f.seriesId === series.id)
    if (idx !== -1) {
      favorites.value.splice(idx, 1)
    } else {
      favorites.value.unshift({
        seriesId: series.id,
        seriesTitle: series.title,
        posterUrl: series.posterUrl,
        genres: series.genres,
        totalEpisodes: series.totalEpisodes ?? 1,
        addedAt: new Date().toISOString(),
      })
    }
    saveToStorage()
  }

  function removeFavorite(seriesId: string) {
    favorites.value = favorites.value.filter(f => f.seriesId !== seriesId)
    saveToStorage()
  }

  function saveWatchHistory(item: WatchHistoryItem) {
    const existingIndex = history.value.findIndex(h => h.seriesId === item.seriesId)
    if (existingIndex !== -1) {
      history.value.splice(existingIndex, 1)
    }
    history.value.unshift(item)
    // Keep max 50 items
    if (history.value.length > 50) {
      history.value.pop()
    }
    saveToStorage()
  }

  function getHistoryItem(seriesId: string): WatchHistoryItem | undefined {
    return history.value.find(h => h.seriesId === seriesId)
  }

  function clearHistory() {
    history.value = []
    saveToStorage()
  }

  return {
    favorites,
    history,
    isFavorite,
    toggleFavorite,
    removeFavorite,
    saveWatchHistory,
    getHistoryItem,
    clearHistory,
  }
})
