<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
import { useToast } from '../../composables/useToast'
import DataTable from '../../components/admin/DataTable.vue'
import StatusBadge from '../../components/admin/StatusBadge.vue'
import Modal from '../../components/common/Modal.vue'
import type { RightsRecord } from '../../types'

const adminStore = useAdminStore()
const toast = useToast()

const selectedRight = ref<RightsRecord | null>(null)
const reviewNotes = ref('')
const showModal = ref(false)

const columns = [
  { key: 'seriesTitle', label: 'Serie Audiovisual', sortable: true },
  { key: 'holderName', label: 'Titular de Derechos / Distribuidora', sortable: true },
  { key: 'licenseType', label: 'Tipo de Licencia' },
  { key: 'validUntil', label: 'Vigencia Hasta', sortable: true },
  { key: 'status', label: 'Estado Legal', align: 'center' as const },
]

onMounted(() => {
  adminStore.fetchRights()
})

function openReview(right: RightsRecord) {
  selectedRight.value = right
  reviewNotes.value = right.notes || ''
  showModal.value = true
}

async function approveRight() {
  if (!selectedRight.value) return
  await adminStore.updateRightStatus(selectedRight.value.id, 'approved', reviewNotes.value)
  toast.success(`Derechos aprobados para "${selectedRight.value.seriesTitle}".`)
  showModal.value = false
}

async function rejectRight() {
  if (!selectedRight.value) return
  await adminStore.updateRightStatus(selectedRight.value.id, 'rejected', reviewNotes.value)
  toast.warning(`Derechos rechazados para "${selectedRight.value.seriesTitle}".`)
  showModal.value = false
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Gestión de Derechos y Licencias
        </h1>
        <p class="text-xs sm:text-sm text-text-muted mt-0.5">
          Verificación legal de contratos y autorizaciones de transmisión vertical para territorio hispano.
        </p>
      </div>
    </div>

    <!-- Rights Table -->
    <DataTable
      :columns="columns"
      :data="adminStore.rights"
      :loading="adminStore.loading"
      searchPlaceholder="Buscar por serie o titular..."
    >
      <template #seriesTitle="{ item }">
        <div>
          <span class="font-bold text-white block">{{ item.seriesTitle }}</span>
          <span class="text-[11px] font-mono text-text-dim">ID: {{ item.id }}</span>
        </div>
      </template>

      <template #licenseType="{ item }">
        <span class="px-2 py-0.5 rounded-md bg-surface-lighter text-text-muted font-mono text-[11px] capitalize">
          {{ item.licenseType }}
        </span>
      </template>

      <template #validUntil="{ value }">
        <span class="font-mono text-xs text-text-muted">
          {{ new Date(value).toLocaleDateString('es-ES') }}
        </span>
      </template>

      <template #status="{ item }">
        <StatusBadge :status="item.status" />
      </template>

      <template #rowActions="{ item }">
        <button
          @click="openReview(item)"
          class="px-3 py-1.5 rounded-lg bg-surface-light hover:bg-surface-lighter text-white text-xs font-semibold border border-surface-border transition-colors"
        >
          Revisar
        </button>
      </template>
    </DataTable>

    <!-- Review Modal -->
    <Modal
      v-model="showModal"
      title="Dictamen de Derechos y Licencia"
      maxWidth="lg"
    >
      <div v-if="selectedRight" class="space-y-4">
        <div class="p-3.5 rounded-xl bg-surface/70 border border-surface-border space-y-2 text-xs">
          <div class="flex justify-between">
            <span class="text-text-muted">Serie:</span>
            <span class="font-bold text-white">{{ selectedRight.seriesTitle }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-text-muted">Titular:</span>
            <span class="font-bold text-white">{{ selectedRight.holderName }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-text-muted">Territorio:</span>
            <span class="font-bold text-white">{{ selectedRight.territory.join(', ') }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-text-muted">Tipo de licencia:</span>
            <span class="font-mono text-secondary font-bold">{{ selectedRight.licenseType }}</span>
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-text-muted mb-1.5 uppercase tracking-wider">
            Notas de Auditoría Legal
          </label>
          <textarea
            v-model="reviewNotes"
            rows="3"
            placeholder="Añade observaciones sobre el contrato, vigencia o cláusulas territoriales..."
            class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
          ></textarea>
        </div>
      </div>

      <template #footer>
        <button
          @click="rejectRight"
          class="px-4 py-2 rounded-xl bg-red-950/60 hover:bg-red-950 text-red-300 text-xs font-semibold border border-red-800/50 transition-colors"
        >
          Rechazar Licencia
        </button>
        <button
          @click="approveRight"
          class="px-5 py-2 rounded-xl bg-green-600 hover:bg-green-500 text-white text-xs font-bold shadow-lg transition-all"
        >
          Aprobar para Emisión
        </button>
      </template>
    </Modal>
  </div>
</template>
