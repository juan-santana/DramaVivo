<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
import { adminService } from '../../services/admin'
import { useToast } from '../../composables/useToast'
import DataTable from '../../components/admin/DataTable.vue'
import StatusBadge from '../../components/admin/StatusBadge.vue'
import FormModal from '../../components/admin/FormModal.vue'
import type { VideoAsset } from '../../types'

const adminStore = useAdminStore()
const toast = useToast()

const showUploadModal = ref(false)
const uploading = ref(false)
const selectedFile = ref<File | null>(null)
const resolution = ref<'1080p' | '720p' | '4k'>('1080p')

const columns = [
  { key: 'filename', label: 'Archivo Multimedia', sortable: true },
  { key: 'resolution', label: 'Resolución', align: 'center' as const },
  { key: 'aspectRatio', label: 'Relación de Aspecto', align: 'center' as const },
  { key: 'format', label: 'Formato', align: 'center' as const },
  { key: 'status', label: 'Estado de Transcodificación', align: 'center' as const },
]

onMounted(() => {
  adminStore.fetchVideos()
})

function onFileSelect(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0]
  }
}

async function handleUpload() {
  if (!selectedFile.value) {
    toast.warning('Por favor selecciona un archivo de video.')
    return
  }

  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('video', selectedFile.value)
    formData.append('filename', selectedFile.value.name)
    formData.append('resolution', resolution.value)

    await adminService.uploadVideo(formData)
    await adminStore.fetchVideos()
    toast.success('Video subido exitosamente. En cola de transcodificación HLS.')
    showUploadModal.value = false
    selectedFile.value = null
  } catch (err: unknown) {
    toast.error(err instanceof Error ? err.message : 'Error al subir el video.')
  } finally {
    uploading.value = false
  }
}

async function handleDeleteVideo(video: VideoAsset) {
  if (confirm(`¿Eliminar el archivo ${video.filename}?`)) {
    await adminService.deleteVideo(video.id)
    await adminStore.fetchVideos()
    toast.info('Video eliminado de los medios.')
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Almacenamiento de Video y Transcodificación
        </h1>
        <p class="text-xs sm:text-sm text-text-muted mt-0.5">
          Gestión de ficheros fuente y generación de perfiles HLS multi-bitrate adaptados a formato 9:16.
        </p>
      </div>

      <button
        @click="showUploadModal = true"
        class="px-4 py-2.5 rounded-xl bg-primary hover:bg-primary-hover text-white text-xs font-bold shadow-glow-primary transition-all flex items-center gap-1.5"
      >
        <span>+ Subir Video Master</span>
      </button>
    </div>

    <!-- Video Table -->
    <DataTable
      :columns="columns"
      :data="adminStore.videos"
      :loading="adminStore.loading"
      searchPlaceholder="Buscar archivo de video..."
    >
      <template #filename="{ item }">
        <div>
          <span class="font-bold text-white block">{{ item.filename }}</span>
          <span class="text-[11px] font-mono text-text-dim">{{ item.storagePath }}</span>
        </div>
      </template>

      <template #resolution="{ value }">
        <span class="px-2 py-0.5 rounded-md bg-surface-lighter font-mono text-xs text-secondary font-bold">
          {{ value }}
        </span>
      </template>

      <template #aspectRatio="{ value }">
        <span class="px-2 py-0.5 rounded-md bg-surface-lighter font-mono text-xs text-white">
          {{ value }} (Vertical)
        </span>
      </template>

      <template #format="{ value }">
        <span class="font-mono text-xs text-text-muted uppercase">
          {{ value }}
        </span>
      </template>

      <template #status="{ item }">
        <div class="flex flex-col items-center gap-1">
          <StatusBadge :status="item.status" />
          <span v-if="item.transcodeProgress" class="text-[10px] text-text-muted font-mono">
            {{ item.transcodeProgress }}% completado
          </span>
        </div>
      </template>

      <template #rowActions="{ item }">
        <button
          @click="handleDeleteVideo(item)"
          class="p-1.5 rounded-lg text-red-400 hover:text-red-300 hover:bg-red-950/40"
          title="Eliminar archivo"
        >
          🗑️
        </button>
      </template>
    </DataTable>

    <!-- Upload Modal -->
    <FormModal
      v-model="showUploadModal"
      title="Subir Video Master para Transcodificación"
      :loading="uploading"
      submitText="Iniciar Carga"
      maxWidth="md"
      @submit="handleUpload"
    >
      <div>
        <label class="block text-xs font-semibold text-text-muted mb-1.5 uppercase tracking-wider">
          Seleccionar Archivo (MP4 / MOV)
        </label>
        <input
          type="file"
          accept="video/mp4,video/quicktime,video/webm"
          @change="onFileSelect"
          class="w-full text-xs text-text-muted file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-primary file:text-white hover:file:bg-primary-hover cursor-pointer"
        />
      </div>

      <div>
        <label class="block text-xs font-semibold text-text-muted mb-1 uppercase tracking-wider">
          Resolución Objetivo
        </label>
        <select
          v-model="resolution"
          class="w-full px-3.5 py-2.5 bg-surface border border-surface-border rounded-xl text-white text-xs focus:outline-none focus:border-primary"
        >
          <option value="1080p">1080x1920 (Full HD Vertical - Recomendado)</option>
          <option value="720p">720x1280 (HD Rápido)</option>
          <option value="4k">4K Ultra HD Vertical</option>
        </select>
      </div>
    </FormModal>
  </div>
</template>
