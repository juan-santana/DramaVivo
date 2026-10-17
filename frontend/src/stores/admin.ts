import { defineStore } from 'pinia'
import { ref } from 'vue'
import type {
  Source,
  ImportJob,
  DiscoveredSeries,
  RightsRecord,
  Series,
  VideoAsset,
  TakedownRequest,
  AnalyticsSummary,
} from '../types'
import { adminService } from '../services/admin'

export const useAdminStore = defineStore('admin', () => {
  const sources = ref<Source[]>([])
  const importJobs = ref<ImportJob[]>([])
  const discovered = ref<DiscoveredSeries[]>([])
  const rights = ref<RightsRecord[]>([])
  const series = ref<Series[]>([])
  const videos = ref<VideoAsset[]>([])
  const takedowns = ref<TakedownRequest[]>([])
  const analytics = ref<AnalyticsSummary | null>(null)

  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchSources() {
    loading.value = true
    try {
      sources.value = await adminService.getSources()
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al cargar fuentes'
    } finally {
      loading.value = false
    }
  }

  async function toggleSource(id: string, enabled: boolean) {
    try {
      await adminService.toggleSource(id, enabled)
      const src = sources.value.find(s => s.id === id)
      if (src) src.enabled = enabled
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al modificar fuente'
    }
  }

  async function triggerScraper(id: string) {
    try {
      const job = await adminService.triggerScraper(id)
      importJobs.value.unshift(job)
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al iniciar raspador'
    }
  }

  async function fetchImportJobs() {
    loading.value = true
    try {
      importJobs.value = await adminService.getImportJobs()
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al cargar trabajos'
    } finally {
      loading.value = false
    }
  }

  async function fetchDiscovered() {
    loading.value = true
    try {
      discovered.value = await adminService.getDiscovered()
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al cargar catálogo descubierto'
    } finally {
      loading.value = false
    }
  }

  async function importDiscovered(id: string) {
    try {
      const newSeries = await adminService.importDiscoveredSeries(id)
      series.value.unshift(newSeries)
      const disc = discovered.value.find(d => d.id === id)
      if (disc) disc.status = 'imported'
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al importar serie'
    }
  }

  async function blockDiscovered(id: string) {
    try {
      await adminService.blockDiscoveredSeries(id)
      const disc = discovered.value.find(d => d.id === id)
      if (disc) disc.status = 'blocked'
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al bloquear serie'
    }
  }

  async function fetchRights() {
    loading.value = true
    try {
      rights.value = await adminService.getRights()
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al cargar derechos'
    } finally {
      loading.value = false
    }
  }

  async function updateRightStatus(id: string, status: RightsRecord['status'], notes?: string) {
    try {
      const updated = await adminService.updateRightStatus(id, status, notes)
      const idx = rights.value.findIndex(r => r.id === id)
      if (idx !== -1) {
        rights.value[idx] = updated
      }
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al actualizar derechos'
    }
  }

  async function fetchSeries() {
    loading.value = true
    try {
      series.value = await adminService.getSeries()
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al cargar series'
    } finally {
      loading.value = false
    }
  }

  async function deleteSeries(id: string) {
    try {
      await adminService.deleteSeries(id)
      series.value = series.value.filter(s => s.id !== id)
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al eliminar serie'
    }
  }

  async function fetchVideos() {
    loading.value = true
    try {
      videos.value = await adminService.getVideos()
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al cargar videos'
    } finally {
      loading.value = false
    }
  }

  async function fetchTakedowns() {
    loading.value = true
    try {
      takedowns.value = await adminService.getTakedowns()
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al cargar reclamaciones'
    } finally {
      loading.value = false
    }
  }

  async function fetchAnalytics() {
    loading.value = true
    try {
      analytics.value = await adminService.getAnalytics()
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Error al cargar analítica'
    } finally {
      loading.value = false
    }
  }

  return {
    sources,
    importJobs,
    discovered,
    rights,
    series,
    videos,
    takedowns,
    analytics,
    loading,
    error,
    fetchSources,
    toggleSource,
    triggerScraper,
    fetchImportJobs,
    fetchDiscovered,
    importDiscovered,
    blockDiscovered,
    fetchRights,
    updateRightStatus,
    fetchSeries,
    deleteSeries,
    fetchVideos,
    fetchTakedowns,
    fetchAnalytics,
  }
})
