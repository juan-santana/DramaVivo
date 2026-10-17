<script setup lang="ts">
import { onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
import DataTable from '../../components/admin/DataTable.vue'
import StatusBadge from '../../components/admin/StatusBadge.vue'

const adminStore = useAdminStore()

const columns = [
  { key: 'sourceName', label: 'Fuente / Conector', sortable: true },
  { key: 'status', label: 'Estado', align: 'center' as const },
  { key: 'recordsDiscovered', label: 'Descubiertos', align: 'center' as const, sortable: true },
  { key: 'recordsImported', label: 'Importados', align: 'center' as const, sortable: true },
  { key: 'recordsSkipped', label: 'Omitidos', align: 'center' as const },
  { key: 'startedAt', label: 'Hora de Inicio', sortable: true },
]

onMounted(() => {
  adminStore.fetchImportJobs()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Historial de Importación
        </h1>
        <p class="text-xs sm:text-sm text-text-muted mt-0.5">
          Auditoría de ejecuciones de raspado automático y registros procesados.
        </p>
      </div>

      <button
        @click="adminStore.fetchImportJobs()"
        class="px-3.5 py-2 rounded-xl bg-surface-light hover:bg-surface-lighter text-text-muted hover:text-white text-xs font-semibold border border-surface-border transition-colors flex items-center gap-1.5"
      >
        <span>↻ Actualizar</span>
      </button>
    </div>

    <!-- Table -->
    <DataTable
      :columns="columns"
      :data="adminStore.importJobs"
      :loading="adminStore.loading"
      searchPlaceholder="Buscar por fuente..."
    >
      <template #sourceName="{ item }">
        <div>
          <span class="font-bold text-white block">{{ item.sourceName }}</span>
          <span class="text-[11px] font-mono text-text-dim">Job ID: {{ item.id }}</span>
          <p v-if="item.errorMessage" class="text-[11px] text-red-400 mt-1">
            ⚠️ {{ item.errorMessage }}
          </p>
        </div>
      </template>

      <template #status="{ item }">
        <StatusBadge :status="item.status" />
      </template>

      <template #recordsDiscovered="{ value }">
        <span class="font-mono text-xs font-bold text-white">{{ value }}</span>
      </template>

      <template #recordsImported="{ value }">
        <span class="font-mono text-xs font-bold text-green-400">+{{ value }}</span>
      </template>

      <template #recordsSkipped="{ value }">
        <span class="font-mono text-xs text-text-dim">{{ value }}</span>
      </template>

      <template #startedAt="{ value }">
        <span class="font-mono text-xs text-text-muted">
          {{ new Date(value).toLocaleString('es-ES') }}
        </span>
      </template>
    </DataTable>
  </div>
</template>
