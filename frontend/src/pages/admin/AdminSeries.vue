<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '../../stores/admin'
import { adminService } from '../../services/admin'
import { useToast } from '../../composables/useToast'
import DataTable from '../../components/admin/DataTable.vue'
import StatusBadge from '../../components/admin/StatusBadge.vue'
import FormModal from '../../components/admin/FormModal.vue'
import type { Series } from '../../types'

const router = useRouter()
const adminStore = useAdminStore()
const toast = useToast()

const showModal = ref(false)
const modalLoading = ref(false)
const isEditing = ref(false)
const editingId = ref<string | null>(null)

const seriesForm = ref({
  title: '',
  synopsis: '',
  posterUrl: '',
  genres: 'Drama, Romance',
  language: 'Español',
  totalEpisodes: 20,
  status: 'ongoing' as Series['status'],
})

const columns = [
  { key: 'title', label: 'Serie', sortable: true },
  { key: 'genres', label: 'Géneros' },
  { key: 'totalEpisodes', label: 'Episodios', align: 'center' as const, sortable: true },
  { key: 'status', label: 'Estado', align: 'center' as const },
  { key: 'rating', label: 'Puntuación', align: 'center' as const, sortable: true },
]

onMounted(() => {
  adminStore.fetchSeries()
})

function openCreate() {
  isEditing.value = false
  editingId.value = null
  seriesForm.value = {
    title: '',
    synopsis: '',
    posterUrl: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=600&q=80',
    genres: 'Drama, Romance',
    language: 'Español',
    totalEpisodes: 30,
    status: 'ongoing',
  }
  showModal.value = true
}

function openEdit(item: Series) {
  isEditing.value = true
  editingId.value = item.id
  seriesForm.value = {
    title: item.title,
    synopsis: item.synopsis,
    posterUrl: item.posterUrl,
    genres: item.genres.join(', '),
    language: item.language || 'es',
    totalEpisodes: item.totalEpisodes || 1,
    status: (item.status as any) || 'completed',
  }
  showModal.value = true
}

async function handleSave() {
  if (!seriesForm.value.title || !seriesForm.value.synopsis) {
    toast.warning('Título y sinopsis son obligatorios.')
    return
  }

  modalLoading.value = true
  try {
    const genresArray = seriesForm.value.genres.split(',').map(g => g.trim()).filter(Boolean)
    const payload = {
      ...seriesForm.value,
      genres: genresArray,
    }

    if (isEditing.value && editingId.value) {
      await adminService.updateSeries(editingId.value, payload)
      toast.success('Serie actualizada correctamente.')
    } else {
      await adminService.createSeries(payload)
      toast.success('Nueva serie registrada.')
    }

    await adminStore.fetchSeries()
    showModal.value = false
  } catch (err: unknown) {
    toast.error(err instanceof Error ? err.message : 'Error al guardar la serie.')
  } finally {
    modalLoading.value = false
  }
}

async function handleDelete(item: Series) {
  if (confirm(`¿Seguro que deseas eliminar la serie "${item.title}"?`)) {
    await adminStore.deleteSeries(item.id)
    toast.info(`Serie "${item.title}" eliminada.`)
  }
}

function manageEpisodes(item: Series) {
  router.push(`/admin/episodios?seriesId=${item.id}`)
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Gestión de Series y Producciones
        </h1>
        <p class="text-xs sm:text-sm text-text-muted mt-0.5">
          Creación, edición y administración de microdramas publicados en la plataforma.
        </p>
      </div>

      <button
        @click="openCreate"
        class="px-4 py-2.5 rounded-xl bg-primary hover:bg-primary-hover text-white text-xs font-bold shadow-glow-primary transition-all flex items-center gap-1.5"
      >
        <span>+ Nueva Serie</span>
      </button>
    </div>

    <!-- Series Table -->
    <DataTable
      :columns="columns"
      :data="adminStore.series"
      :loading="adminStore.loading"
      searchPlaceholder="Buscar por título o género..."
    >
      <template #title="{ item }">
        <div class="flex items-center gap-3">
          <img :src="item.posterUrl" :alt="item.title" class="w-10 aspect-[2/3] rounded-md object-cover" />
          <div class="min-w-0">
            <span class="font-bold text-white block truncate">{{ item.title }}</span>
            <span class="text-[11px] text-text-dim">Slug: {{ item.slug }}</span>
          </div>
        </div>
      </template>

      <template #genres="{ item }">
        <div class="flex flex-wrap gap-1">
          <span
            v-for="g in item.genres"
            :key="g"
            class="px-1.5 py-0.2 rounded bg-surface-lighter text-text-muted text-[10px]"
          >
            {{ g }}
          </span>
        </div>
      </template>

      <template #totalEpisodes="{ value }">
        <span class="font-mono text-xs font-bold text-white">{{ value }} eps</span>
      </template>

      <template #status="{ item }">
        <StatusBadge :status="(item.status as any) || 'completed'" />
      </template>

      <template #rating="{ item }">
        <span class="font-mono text-xs font-bold text-secondary">
          ★ {{ item.rating?.toFixed(1) || '5.0' }}
        </span>
      </template>

      <template #rowActions="{ item }">
        <div class="flex items-center justify-end gap-1.5">
          <button
            @click="manageEpisodes(item)"
            class="px-2.5 py-1.5 rounded-lg bg-surface-light hover:bg-surface-lighter text-secondary text-xs font-semibold border border-surface-border transition-colors"
            title="Gestionar Capítulos"
          >
            Episodios
          </button>
          <button
            @click="openEdit(item)"
            class="p-1.5 rounded-lg text-text-muted hover:text-white hover:bg-surface-light"
            title="Editar serie"
          >
            ✏️
          </button>
          <button
            @click="handleDelete(item)"
            class="p-1.5 rounded-lg text-red-400 hover:text-red-300 hover:bg-red-950/40"
            title="Eliminar serie"
          >
            🗑️
          </button>
        </div>
      </template>
    </DataTable>

    <!-- Create / Edit Modal -->
    <FormModal
      v-model="showModal"
      :title="isEditing ? 'Editar Serie' : 'Registrar Nueva Serie'"
      :loading="modalLoading"
      :submitText="isEditing ? 'Actualizar Serie' : 'Crear Serie'"
      maxWidth="lg"
      @submit="handleSave"
    >
      <div>
        <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
          Título Oficial
        </label>
        <input
          v-model="seriesForm.title"
          type="text"
          required
          placeholder="p. ej. El Secreto del Magnate"
          class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
        />
      </div>

      <div>
        <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
          Sinopsis
        </label>
        <textarea
          v-model="seriesForm.synopsis"
          rows="3"
          required
          placeholder="Escribe la trama del microdrama..."
          class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
        ></textarea>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
            Géneros (separados por coma)
          </label>
          <input
            v-model="seriesForm.genres"
            type="text"
            placeholder="Romance, Venganza, Drama"
            class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
            Total de Episodios
          </label>
          <input
            v-model.number="seriesForm.totalEpisodes"
            type="number"
            min="1"
            class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
          />
        </div>
      </div>

      <div>
        <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
          URL del Póster Vertical
        </label>
        <input
          v-model="seriesForm.posterUrl"
          type="url"
          required
          class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary font-mono"
        />
      </div>

      <div>
        <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
          Estado
        </label>
        <select
          v-model="seriesForm.status"
          class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
        >
          <option value="ongoing">En emisión</option>
          <option value="completed">Completa</option>
          <option value="announced">Próximamente</option>
        </select>
      </div>
    </FormModal>
  </div>
</template>
