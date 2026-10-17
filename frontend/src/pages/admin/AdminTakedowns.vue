<script setup lang="ts">
import { onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
import { adminService } from '../../services/admin'
import { useToast } from '../../composables/useToast'
import DataTable from '../../components/admin/DataTable.vue'
import StatusBadge from '../../components/admin/StatusBadge.vue'
import type { TakedownRequest } from '../../types'

const adminStore = useAdminStore()
const toast = useToast()

const columns = [
  { key: 'seriesTitle', label: 'Serie Reclamada', sortable: true },
  { key: 'claimantName', label: 'Reclamante / Titular', sortable: true },
  { key: 'reason', label: 'Motivo de la Reclamación' },
  { key: 'status', label: 'Estado', align: 'center' as const },
  { key: 'createdAt', label: 'Fecha de Entrada', sortable: true },
]

onMounted(() => {
  adminStore.fetchTakedowns()
})

async function resolveTakedown(item: TakedownRequest) {
  await adminService.updateTakedownStatus(item.id, 'resolved', 'Contenido verificado con el titular.')
  await adminStore.fetchTakedowns()
  toast.success(`Reclamación de "${item.seriesTitle}" marcada como resuelta.`)
}

async function rejectTakedown(item: TakedownRequest) {
  await adminService.updateTakedownStatus(item.id, 'rejected', 'Falta de acreditación suficiente de derechos.')
  await adminStore.fetchTakedowns()
  toast.info(`Reclamación desestimada.`)
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Reclamaciones de Retirada (DMCA)
        </h1>
        <p class="text-xs sm:text-sm text-text-muted mt-0.5">
          Atención expedita a avisos de infracción de propiedad intelectual y disputas de licencias.
        </p>
      </div>
    </div>

    <!-- Takedowns Table -->
    <DataTable
      :columns="columns"
      :data="adminStore.takedowns"
      :loading="adminStore.loading"
      searchPlaceholder="Buscar por reclamante o serie..."
    >
      <template #seriesTitle="{ item }">
        <div>
          <span class="font-bold text-white block">{{ item.seriesTitle }}</span>
          <span class="text-[11px] font-mono text-text-dim">ID: {{ item.id }}</span>
        </div>
      </template>

      <template #claimantName="{ item }">
        <div>
          <span class="text-white font-medium block">{{ item.claimantName }}</span>
          <span class="text-[11px] text-text-muted">{{ item.claimantEmail }}</span>
          <span v-if="item.organization" class="text-[10px] text-text-dim block">({{ item.organization }})</span>
        </div>
      </template>

      <template #reason="{ value }">
        <p class="text-xs text-text-muted line-clamp-2 max-w-sm">
          {{ value }}
        </p>
      </template>

      <template #status="{ item }">
        <StatusBadge :status="item.status" />
      </template>

      <template #createdAt="{ value }">
        <span class="font-mono text-xs text-text-muted">
          {{ new Date(value).toLocaleDateString('es-ES') }}
        </span>
      </template>

      <template #rowActions="{ item }">
        <div v-if="item.status === 'pending'" class="flex items-center justify-end gap-2">
          <button
            @click="rejectTakedown(item)"
            class="px-2.5 py-1 rounded-lg bg-surface-light hover:bg-surface-lighter text-text-muted text-xs font-semibold border border-surface-border"
          >
            Desestimar
          </button>
          <button
            @click="resolveTakedown(item)"
            class="px-3 py-1 rounded-lg bg-green-600 hover:bg-green-500 text-white text-xs font-bold"
          >
            Resolver
          </button>
        </div>
      </template>
    </DataTable>
  </div>
</template>
