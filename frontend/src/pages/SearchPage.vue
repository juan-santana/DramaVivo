<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useHead } from '@unhead/vue'
import { seriesService } from '../services/series'
import type { Series } from '../types'
import { useI18n } from '../i18n'
import SearchBar from '../components/common/SearchBar.vue'
import SeriesGrid from '../components/catalog/SeriesGrid.vue'
import AdSlot from '../components/ads/AdSlot.vue'

const { t, currentLang } = useI18n()

useHead({
  title: 'Búsqueda de Microdramas - DramaApp',
  meta: [
    {
      name: 'description',
      content: 'Busca al instante entre cientos de episodios de microdramas y series en formato vertical.',
    },
  ],
})

const query = ref('')
const results = ref<Series[]>([])
const loading = ref(false)
const hasSearched = ref(false)

const popularSearches = computed(() => {
  if (currentLang.value === 'en') {
    return ['Billionaire', 'Mafia', 'Revenge', 'Surrogate', 'Secret Lover', 'Heiress']
  }
  return ['Venganza', 'CEO', 'Heredera', 'Multimillonario', 'Amor prohibido', 'Matrimonio']
})

async function performSearch(val: string) {
  query.value = val
  if (!val.trim()) {
    results.value = []
    hasSearched.value = false
    return
  }

  loading.value = true
  hasSearched.value = true
  try {
    const res = await seriesService.search(val)
    results.value = res.series
  } catch {
    results.value = []
  } finally {
    loading.value = false
  }
}

function quickSearch(term: string) {
  query.value = term
  performSearch(term)
}

onMounted(() => {
  // Pre-load initial suggestions
  seriesService.getTrending().then(data => {
    if (!hasSearched.value) {
      results.value = data
    }
  })
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
    <div class="max-w-2xl mx-auto text-center space-y-4">
      <h1 class="text-3xl sm:text-4xl font-black text-white tracking-tight">
        {{ t('search.title') }}
      </h1>
      <p class="text-xs sm:text-sm text-text-muted">
        {{ t('search.subtitle') }}
      </p>

      <!-- Search Input -->
      <div class="pt-2">
        <SearchBar
          :modelValue="query"
          :placeholder="t('search.inputPlaceholder')"
          :autoFocus="true"
          @search="performSearch"
        />
      </div>

      <!-- Popular keywords -->
      <div class="flex flex-wrap items-center justify-center gap-2 pt-2">
        <span class="text-xs text-text-dim">{{ t('search.recentSearches') }}</span>
        <button
          v-for="term in popularSearches"
          :key="term"
          @click="quickSearch(term)"
          class="px-2.5 py-1 rounded-full text-xs font-medium bg-surface hover:bg-surface-light border border-surface-border text-text-muted hover:text-white transition-colors"
        >
          {{ term }}
        </button>
      </div>
    </div>

    <!-- Search Results Header -->
    <div class="flex items-center justify-between border-b border-surface-border pb-3">
      <h3 class="text-base sm:text-lg font-bold text-white">
        {{ hasSearched ? `${t('search.resultsFor')} "${query}" (${results.length})` : (currentLang === 'en' ? 'Recommended Dramas' : 'Dramas Recomendados') }}
      </h3>
    </div>

    <!-- Results Grid -->
    <SeriesGrid
      :series="results"
      :loading="loading"
      :emptyMessage="hasSearched ? `${t('search.noDramas')} ${t('search.tryDifferent')}` : t('search.noDramas')"
    />

    <!-- Ad banner -->
    <AdSlot />
  </div>
</template>
