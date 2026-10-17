import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Series, Genre } from '../types'
import { seriesService } from '../services/series'

export const useCatalogStore = defineStore('catalog', () => {
  const series = ref<Series[]>([])
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(36)
  const totalPages = ref(1)

  const featured = ref<Series[]>([])
  const trending = ref<Series[]>([])
  const recent = ref<Series[]>([])
  const genres = ref<Genre[]>([])

  const selectedGenre = ref<string>('todos')
  const selectedSort = ref<'recent' | 'popular' | 'rating'>('recent')
  const selectedLanguage = ref<string>('todos')
  const searchQuery = ref<string>('')

  const loading = ref(false)
  const loadingHome = ref(false)
  const error = ref<string | null>(null)

  async function fetchCatalog(resetPage = false) {
    if (resetPage) {
      page.value = 1
    }
    loading.value = true
    error.value = null
    try {
      const res = await seriesService.getAll({
        page: page.value,
        pageSize: pageSize.value,
        genre: selectedGenre.value === 'todos' ? undefined : selectedGenre.value,
        sort: selectedSort.value,
        search: searchQuery.value ? searchQuery.value : undefined,
        language: selectedLanguage.value === 'todos' ? undefined : selectedLanguage.value,
      })
      series.value = res.data
      total.value = res.total
      totalPages.value = res.totalPages
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al cargar catálogo'
    } finally {
      loading.value = false
    }
  }

  async function fetchHomeData() {
    loadingHome.value = true
    try {
      const [featRes, trendRes, recRes, genRes] = await Promise.all([
        seriesService.getFeatured(),
        seriesService.getTrending(),
        seriesService.getRecent(10),
        seriesService.getGenres(),
      ])
      featured.value = featRes
      trending.value = trendRes
      recent.value = recRes
      genres.value = genRes
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al cargar página de inicio'
    } finally {
      loadingHome.value = false
    }
  }

  async function fetchGenres() {
    if (genres.value.length === 0) {
      genres.value = await seriesService.getGenres()
    }
  }

  function setGenre(genre: string) {
    selectedGenre.value = genre
    fetchCatalog(true)
  }

  function setSort(sort: 'recent' | 'popular' | 'rating') {
    selectedSort.value = sort
    fetchCatalog(true)
  }

  function setSearch(query: string) {
    searchQuery.value = query
    fetchCatalog(true)
  }

  function setPage(p: number) {
    page.value = p
    fetchCatalog(false)
  }

  return {
    series,
    total,
    page,
    pageSize,
    totalPages,
    featured,
    trending,
    recent,
    genres,
    selectedGenre,
    selectedSort,
    selectedLanguage,
    searchQuery,
    loading,
    loadingHome,
    error,
    fetchCatalog,
    fetchHomeData,
    fetchGenres,
    setGenre,
    setSort,
    setSearch,
    setPage,
  }
})
