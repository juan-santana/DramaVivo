<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHead } from '@unhead/vue'
import { useCatalogStore } from '../stores/catalog'
import { useI18n } from '../i18n'
import SearchBar from '../components/common/SearchBar.vue'
import GenreFilter from '../components/catalog/GenreFilter.vue'
import SeriesGrid from '../components/catalog/SeriesGrid.vue'
import Pagination from '../components/common/Pagination.vue'
import AdSlot from '../components/ads/AdSlot.vue'

const route = useRoute()
const router = useRouter()
const catalogStore = useCatalogStore()
const { t } = useI18n()

useHead({
  title: 'Catálogo de Microdramas - DramaApp',
  meta: [
    {
      name: 'description',
      content: 'Explora todos los microdramas y series verticales en español e inglés. Filtra por géneros como romance, venganza, multimillonarios y suspenso.',
    },
  ],
})

function syncFromQuery() {
  const genreParam = (route.query.genre as string) || 'todos'
  const sortParam = (route.query.sort as 'recent' | 'popular' | 'rating') || 'recent'
  const searchParam = (route.query.q as string) || ''
  const pageParam = Number(route.query.page) || 1

  catalogStore.selectedGenre = genreParam
  catalogStore.selectedSort = sortParam
  catalogStore.searchQuery = searchParam
  catalogStore.page = pageParam
  catalogStore.fetchCatalog()
}

onMounted(async () => {
  await catalogStore.fetchGenres()
  syncFromQuery()
})

watch(
  () => route.query,
  () => {
    syncFromQuery()
  }
)

function updateRoute() {
  const query: Record<string, string | number> = {}
  if (catalogStore.selectedGenre && catalogStore.selectedGenre !== 'todos') {
    query.genre = catalogStore.selectedGenre
  }
  if (catalogStore.selectedSort && catalogStore.selectedSort !== 'recent') {
    query.sort = catalogStore.selectedSort
  }
  if (catalogStore.searchQuery) {
    query.q = catalogStore.searchQuery
  }
  if (catalogStore.page > 1) {
    query.page = catalogStore.page
  }
  router.push({ query })
}

function onGenreSelect(genre: string) {
  catalogStore.selectedGenre = genre
  catalogStore.page = 1
  updateRoute()
}

function onSortChange(e: Event) {
  const target = e.target as HTMLSelectElement
  catalogStore.selectedSort = target.value as 'recent' | 'popular' | 'rating'
  catalogStore.page = 1
  updateRoute()
}

function onLanguageChange(e: Event) {
  const target = e.target as HTMLSelectElement
  catalogStore.selectedLanguage = target.value
  catalogStore.page = 1
  catalogStore.fetchCatalog()
}

function onSearch(query: string) {
  catalogStore.searchQuery = query
  catalogStore.page = 1
  updateRoute()
}

function onPageChange(page: number) {
  catalogStore.page = page
  updateRoute()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
    <!-- Header title -->
    <div class="space-y-2">
      <h1 class="text-3xl sm:text-4xl font-black text-white tracking-tight">
        {{ t('catalog.title') }}
      </h1>
      <p class="text-sm text-text-muted">
        {{ t('catalog.subtitle') }}
      </p>
    </div>

    <!-- Filters and Search Toolbar -->
    <div class="glass-panel p-4 sm:p-5 rounded-2xl border border-surface-border space-y-4">
      <div class="flex flex-col md:flex-row items-center gap-3">
        <!-- Search bar -->
        <div class="w-full md:flex-1">
          <SearchBar
            :modelValue="catalogStore.searchQuery"
            :placeholder="t('catalog.searchPlaceholder')"
            @search="onSearch"
          />
        </div>

        <!-- Filter Dropdowns -->
        <div class="w-full md:w-auto flex items-center gap-2.5">
          <!-- Sort Dropdown -->
          <div class="relative flex-1 md:w-44">
            <select
              :value="catalogStore.selectedSort"
              @change="onSortChange"
              class="w-full px-3.5 py-3 rounded-xl bg-surface border border-surface-border text-xs font-semibold text-white focus:outline-none focus:border-primary appearance-none cursor-pointer"
            >
              <option value="recent">{{ t('catalog.newest') }}</option>
              <option value="popular">{{ t('catalog.popular') }}</option>
              <option value="rating">{{ t('catalog.rating') }}</option>
            </select>
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-text-muted">
              ▼
            </div>
          </div>

          <!-- Language Dropdown -->
          <div class="relative flex-1 md:w-44">
            <select
              :value="catalogStore.selectedLanguage"
              @change="onLanguageChange"
              class="w-full px-3.5 py-3 rounded-xl bg-surface border border-surface-border text-xs font-semibold text-white focus:outline-none focus:border-primary appearance-none cursor-pointer"
            >
              <option value="todos">{{ t('catalog.langAll') }}</option>
              <option value="Español">{{ t('catalog.langEs') }}</option>
              <option value="English">{{ t('catalog.langEn') }}</option>
            </select>
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-text-muted">
              ▼
            </div>
          </div>
        </div>
      </div>

      <!-- Genre Filter Pills -->
      <div class="pt-2 border-t border-surface-border/50">
        <GenreFilter
          :genres="catalogStore.genres"
          :selectedGenre="catalogStore.selectedGenre"
          @select="onGenreSelect"
        />
      </div>
    </div>

    <!-- Active Filters Summary -->
    <div class="flex items-center justify-between text-xs text-text-muted px-1">
      <p>
        <span class="font-bold text-white">{{ catalogStore.series.length }}</span> {{ t('catalog.seriesFound') }}
        <span v-if="catalogStore.selectedGenre !== 'todos'"> • "{{ catalogStore.selectedGenre }}"</span>
      </p>

      <button
        v-if="catalogStore.selectedGenre !== 'todos' || catalogStore.searchQuery || catalogStore.selectedLanguage !== 'todos'"
        @click="onGenreSelect('todos'); onSearch(''); catalogStore.selectedLanguage = 'todos'; catalogStore.fetchCatalog()"
        class="text-primary hover:underline font-semibold"
      >
        {{ t('catalog.clearFilters') }}
      </button>
    </div>

    <!-- Series Grid -->
    <SeriesGrid
      :series="catalogStore.series"
      :loading="catalogStore.loading"
      :emptyMessage="t('catalog.noResults')"
    />

    <!-- Pagination -->
    <Pagination
      v-if="!catalogStore.loading && catalogStore.totalPages > 1"
      :currentPage="catalogStore.page"
      :totalPages="catalogStore.totalPages"
      :totalItems="catalogStore.total"
      @change="onPageChange"
    />

    <!-- Promotional Ad Slot -->
    <AdSlot />
  </div>
</template>
