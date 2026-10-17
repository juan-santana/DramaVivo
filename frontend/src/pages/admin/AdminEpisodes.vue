<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAdminStore } from '../../stores/admin'
import { adminService } from '../../services/admin'
import { useToast } from '../../composables/useToast'
import DataTable from '../../components/admin/DataTable.vue'
import FormModal from '../../components/admin/FormModal.vue'
import type { Episode } from '../../types'

const route = useRoute()
const adminStore = useAdminStore()
const toast = useToast()

const selectedSeriesId = ref<string>('')
const episodes = ref<Episode[]>([])
const loading = ref(false)

const showModal = ref(false)
const modalLoading = ref(false)
const isEditing = ref(false)
const editingId = ref<string | null>(null)

const epForm = ref({
  episodeNumber: 1,
  title: '',
  synopsis: '',
  duration: 120,
  videoUrl: '',
  thumbnailUrl: '',
  isFree: false,
})

const columns = [
  { key: 'episodeNumber', label: 'Capítulo', sortable: true, align: 'center' as const },
  { key: 'title', label: 'Título del Episodio', sortable: true },
  { key: 'duration', label: 'Duración', align: 'center' as const },
  { key: 'isFree', label: 'Acceso Libre', align: 'center' as const },
]

async function loadEpisodes() {
  if (!selectedSeriesId.value) {
    episodes.value = []
    return
  }
  loading.value = true
  try {
    episodes.value = await adminService.getEpisodes(selectedSeriesId.value)
  } catch (err: unknown) {
    toast.error(err instanceof Error ? err.message : 'Error al cargar episodios.')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await adminStore.fetchSeries()
  const qId = (route.query.seriesId as string) || (adminStore.series[0]?.id || '')
  selectedSeriesId.value = qId
  loadEpisodes()
})

watch(selectedSeriesId, () => {
  loadEpisodes()
})

function openCreate() {
  isEditing.value = false
  editingId.value = null
  const nextNum = episodes.value.length + 1
  epForm.value = {
    episodeNumber: nextNum,
    title: `Capítulo ${nextNum}`,
    synopsis: '',
    duration: 120,
    videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
    thumbnailUrl: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80',
    isFree: nextNum <= 2,
  }
  showModal.value = true
}

function openEdit(ep: Episode) {
  isEditing.value = true
  editingId.value = ep.id
  epForm.value = {
    episodeNumber: ep.episodeNumber,
    title: ep.title,
    synopsis: ep.synopsis || '',
    duration: ep.duration,
    videoUrl: ep.videoUrl,
    thumbnailUrl: ep.thumbnailUrl || '',
    isFree: !!ep.isFree,
  }
  showModal.value = true
}

async function handleSave() {
  if (!selectedSeriesId.value) return
  if (!epForm.value.title || !epForm.value.videoUrl) {
    toast.warning('Título y URL de video son obligatorios.')
    return
  }

  modalLoading.value = true
  try {
    if (isEditing.value && editingId.value) {
      await adminService.updateEpisode(selectedSeriesId.value, editingId.value, epForm.value)
      toast.success('Episodio actualizado correctamente.')
    } else {
      await adminService.createEpisode(selectedSeriesId.value, epForm.value)
      toast.success('Episodio añadido con éxito.')
    }
    await loadEpisodes()
    showModal.value = false
  } catch (err: unknown) {
    toast.error(err instanceof Error ? err.message : 'Error al guardar episodio.')
  } finally {
    modalLoading.value = false
  }
}

async function handleDelete(ep: Episode) {
  if (!selectedSeriesId.value) return
  if (confirm(`¿Eliminar el capítulo ${ep.episodeNumber}?`)) {
    await adminService.deleteEpisode(selectedSeriesId.value, ep.id)
    await loadEpisodes()
    toast.info('Episodio eliminado.')
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Gestor de Episodios
        </h1>
        <p class="text-xs sm:text-sm text-text-muted mt-0.5">
          Organiza las secuencias de capítulos, duración y enlaces de video para cada microdrama.
        </p>
      </div>

      <div class="flex items-center gap-3 w-full sm:w-auto">
        <!-- Series Selector -->
        <select
          v-model="selectedSeriesId"
          class="flex-1 sm:w-64 px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs font-semibold focus:outline-none focus:border-primary"
        >
          <option v-for="s in adminStore.series" :key="s.id" :value="s.id">
            {{ s.title }}
          </option>
        </select>

        <button
          @click="openCreate"
          :disabled="!selectedSeriesId"
          class="shrink-0 px-4 py-2.5 rounded-xl bg-primary hover:bg-primary-hover text-white text-xs font-bold shadow-glow-primary transition-all disabled:opacity-50"
        >
          + Añadir Episodio
        </button>
      </div>
    </div>

    <!-- Episode Table -->
    <DataTable
      :columns="columns"
      :data="episodes"
      :loading="loading"
      searchPlaceholder="Buscar episodio..."
    >
      <template #episodeNumber="{ value }">
        <span class="font-mono text-xs font-bold text-primary">EP {{ value }}</span>
      </template>

      <template #title="{ item }">
        <div>
          <span class="font-bold text-white block">{{ item.title }}</span>
          <span class="text-[11px] font-mono text-text-dim truncate max-w-xs block" :title="item.videoUrl">
            {{ item.videoUrl }}
          </span>
        </div>
      </template>

      <template #duration="{ value }">
        <span class="font-mono text-xs text-text-muted">
          {{ Math.floor(value / 60) }}:{{ (value % 60) < 10 ? '0' : '' }}{{ value % 60 }} min
        </span>
      </template>

      <template #isFree="{ value }">
        <span
          :class="[
            'px-2 py-0.5 rounded text-[10px] font-bold uppercase',
            value ? 'bg-green-950 text-green-300 border border-green-700/40' : 'bg-surface-lighter text-text-dim'
          ]"
        >
          {{ value ? 'Gratis' : 'VIP' }}
        </span>
      </template>

      <template #rowActions="{ item }">
        <div class="flex items-center justify-end gap-1.5">
          <button
            @click="openEdit(item)"
            class="p-1.5 rounded-lg text-text-muted hover:text-white hover:bg-surface-light"
            title="Editar episodio"
          >
            ✏️
          </button>
          <button
            @click="handleDelete(item)"
            class="p-1.5 rounded-lg text-red-400 hover:text-red-300 hover:bg-red-950/40"
            title="Eliminar episodio"
          >
            🗑️
          </button>
        </div>
      </template>
    </DataTable>

    <!-- Create/Edit Episode Modal -->
    <FormModal
      v-model="showModal"
      :title="isEditing ? 'Editar Episodio' : 'Añadir Nuevo Episodio'"
      :loading="modalLoading"
      :submitText="isEditing ? 'Actualizar' : 'Guardar Episodio'"
      maxWidth="md"
      @submit="handleSave"
    >
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
            Número de Capítulo
          </label>
          <input
            v-model.number="epForm.episodeNumber"
            type="number"
            min="1"
            required
            class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
            Duración (segundos)
          </label>
          <input
            v-model.number="epForm.duration"
            type="number"
            min="10"
            required
            class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
          />
        </div>
      </div>

      <div>
        <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
          Título del Capítulo
        </label>
        <input
          v-model="epForm.title"
          type="text"
          required
          class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
        />
      </div>

      <div>
        <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
          URL del Video (MP4 o HLS .m3u8)
        </label>
        <input
          v-model="epForm.videoUrl"
          type="url"
          required
          class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary font-mono"
        />
      </div>

      <div>
        <label class="flex items-center gap-2 cursor-pointer pt-2">
          <input
            v-model="epForm.isFree"
            type="checkbox"
            class="w-4 h-4 rounded text-primary focus:ring-primary bg-surface border-surface-border"
          />
          <span class="text-xs text-white font-medium">Episodio de acceso gratuito (muestra para nuevos espectadores)</span>
        </label>
      </div>
    </FormModal>
  </div>
</template>
