<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: string
  label?: string
}>()

const statusConfig = computed(() => {
  const s = props.status.toLowerCase()
  switch (s) {
    case 'approved':
    case 'success':
    case 'completed':
    case 'ready':
    case 'active':
      return {
        bg: 'bg-green-950/70 border-green-700/40 text-green-300',
        dot: 'bg-green-400',
        defaultLabel: s === 'approved' ? 'Aprobado' : s === 'completed' ? 'Completado' : 'Listo',
      }
    case 'pending':
    case 'running':
    case 'processing':
    case 'uploading':
    case 'under_review':
      return {
        bg: 'bg-yellow-950/70 border-yellow-700/40 text-yellow-300',
        dot: 'bg-yellow-400 animate-pulse',
        defaultLabel: s === 'pending' ? 'Pendiente' : s === 'running' ? 'En ejecución' : 'Procesando',
      }
    case 'rejected':
    case 'failed':
    case 'blocked':
      return {
        bg: 'bg-red-950/70 border-red-700/40 text-red-300',
        dot: 'bg-red-400',
        defaultLabel: s === 'rejected' ? 'Rechazado' : s === 'failed' ? 'Fallido' : 'Bloqueado',
      }
    case 'idle':
    case 'ongoing':
    default:
      return {
        bg: 'bg-surface-lighter border-surface-border text-text-muted',
        dot: 'bg-text-dim',
        defaultLabel: s === 'ongoing' ? 'En emisión' : 'Inactivo',
      }
  }
})
</script>

<template>
  <span
    :class="[
      'inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border',
      statusConfig.bg
    ]"
  >
    <span :class="['w-1.5 h-1.5 rounded-full', statusConfig.dot]"></span>
    <span>{{ label || statusConfig.defaultLabel }}</span>
  </span>
</template>
