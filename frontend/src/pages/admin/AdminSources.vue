<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
import { adminService } from '../../services/admin'
import { useToast } from '../../composables/useToast'
import DataTable from '../../components/admin/DataTable.vue'
import StatusBadge from '../../components/admin/StatusBadge.vue'
import FormModal from '../../components/admin/FormModal.vue'
import type { Source } from '../../types'

const adminStore = useAdminStore()
const toast = useToast()

const showCreateModal = ref(false)
const modalLoading = ref(false)

const newSource = ref({
  name: '',
  baseUrl: '',
  scraperType: 'REST API',
  enabled: true,
})

const columns = [
  { key: 'name', label: 'Nombre de la Fuente', sortable: true },
  { key: 'scraperType', label: 'Tipo de Motor', sortable: true },
  { key: 'baseUrl', label: 'URL Endpoint / Feed' },
  { key: 'enabled', label: 'Estado', align: 'center' as const },
  { key: 'lastRunStatus', label: 'Última Ejecución', align: 'center' as const },
]

onMounted(() => {
  adminStore.fetchSources()
})

async function toggleSource(item: Source) {
  await adminStore.toggleSource(item.id, !item.enabled)
  toast.info(`Fuente "${item.name}" ${!item.enabled ? 'activada' : 'desactivada'}.`)
}

async function runScraper(item: Source) {
  toast.info(`Iniciando extracción para "${item.name}"...`)
  await adminStore.triggerScraper(item.id)
  toast.success(`Trabajo de importación creado para "${item.name}".`)
}

async function handleCreateSource() {
  if (!newSource.value.name || !newSource.value.baseUrl) {
    toast.warning('Completa el nombre y la URL.')
    return
  }

  modalLoading.value = true
  try {
    await adminService.createSource(newSource.value)
    await adminStore.fetchSources()
    toast.success('Fuente de raspado añadida exitosamente.')
    showCreateModal.value = false
    newSource.value = {
      name: '',
      baseUrl: '',
      scraperType: 'REST API',
      enabled: true,
    }
  } catch (err: unknown) {
    toast.error(err instanceof Error ? err.message : 'Error al crear la fuente.')
  } finally {
    modalLoading.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Fuentes de Raspado y Conectores
        </h1>
        <p class="text-xs sm:text-sm text-text-muted mt-0.5">
          Configura y automatiza la recolección de microdramas desde APIs y feeds externos.
        </p>
      </div>

      <button
        @click="showCreateModal = true"
        class="px-4 py-2.5 rounded-xl bg-primary hover:bg-primary-hover text-white text-xs font-bold shadow-glow-primary transition-all flex items-center gap-1.5"
      >
        <span>+ Nueva Fuente</span>
      </button>
    </div>

    <!-- Data Table -->
    <DataTable
      :columns="columns"
      :data="adminStore.sources"
      :loading="adminStore.loading"
      searchPlaceholder="Buscar por nombre o tipo..."
    >
      <!-- Name slot -->
      <template #name="{ item }">
        <div>
          <span class="font-bold text-white block">{{ item.name }}</span>
          <span class="text-[11px] text-text-dim">ID: {{ item.id }}</span>
        </div>
      </template>

      <!-- Scraper Type slot -->
      <template #scraperType="{ item }">
        <span class="px-2 py-0.5 rounded-md bg-surface-lighter text-text-muted font-mono text-[11px]">
          {{ item.scraperType }}
        </span>
      </template>

      <!-- Base URL slot -->
      <template #baseUrl="{ item }">
        <span class="font-mono text-xs text-text-muted truncate max-w-xs block" :title="item.baseUrl">
          {{ item.baseUrl }}
        </span>
      </template>

      <!-- Enabled toggle slot -->
      <template #enabled="{ item }">
        <button
          @click="toggleSource(item)"
          :class="[
            'px-2.5 py-1 rounded-full text-[11px] font-semibold transition-colors border',
            item.enabled
              ? 'bg-green-950/60 border-green-700/40 text-green-300'
              : 'bg-red-950/60 border-red-700/40 text-red-300'
          ]"
        >
          {{ item.enabled ? 'Activa' : 'Inactiva' }}
        </button>
      </template>

      <!-- Last Run Status slot -->
      <template #lastRunStatus="{ item }">
        <StatusBadge :status="item.lastRunStatus || 'idle'" />
      </template>

      <!-- Row actions -->
      <template #rowActions="{ item }">
        <div class="flex items-center justify-end gap-2">
          <button
            @click="runScraper(item)"
            class="px-2.5 py-1.5 rounded-lg bg-surface-light hover:bg-primary hover:text-white text-text-muted text-xs font-semibold border border-surface-border transition-all"
            title="Ejecutar ahora"
          >
            ▶ Ejecutar
          </button>
        </div>
      </template>
    </DataTable>

    <!-- Create Modal -->
    <FormModal
      v-model="showCreateModal"
      title="Añadir Nueva Fuente de Raspado"
      :loading="modalLoading"
      submitText="Guardar Fuente"
      @submit="handleCreateSource"
    >
      <div>
        <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
          Nombre Identificador
        </label>
        <input
          v-model="newSource.name"
          type="text"
          required
          placeholder="p. ej. DramaFlix Feed V2"
          class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
        />
      </div>

      <div>
        <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
          Tipo de Motor
        </label>
        <select
          v-model="newSource.scraperType"
          class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
        >
          <option value="REST API">REST API JSON</option>
          <option value="HTML Puppeteer">HTML Headless Scraper</option>
          <option value="RSS XML Feed">RSS / XML Media Feed</option>
        </select>
      </div>

      <div>
        <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
          URL Base / Endpoint
        </label>
        <input
          v-model="newSource.baseUrl"
          type="url"
          required
          placeholder="https://api.ejemplo.com/dramas"
          class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary font-mono"
        />
      </div>
    </FormModal>
  </div>
</template>
