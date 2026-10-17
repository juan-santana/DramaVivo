<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  currentPage: number
  totalPages: number
  totalItems?: number
}>()

const emit = defineEmits<{
  (e: 'change', page: number): void
}>()

const visiblePages = computed(() => {
  const current = props.currentPage
  const total = props.totalPages
  const pages: (number | string)[] = []

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) {
      pages.push('...')
    }
    const start = Math.max(2, current - 1)
    const end = Math.min(total - 1, current + 1)
    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
    if (current < total - 2) {
      pages.push('...')
    }
    pages.push(total)
  }

  return pages
})

function goTo(page: number) {
  if (page >= 1 && page <= props.totalPages && page !== props.currentPage) {
    emit('change', page)
  }
}
</script>

<template>
  <div v-if="totalPages > 1" class="flex flex-col sm:flex-row items-center justify-between gap-4 py-6">
    <p v-if="totalItems !== undefined" class="text-xs text-text-muted">
      Mostrando página <span class="font-semibold text-white">{{ currentPage }}</span> de <span class="font-semibold text-white">{{ totalPages }}</span> ({{ totalItems }} resultados)
    </p>

    <div class="flex items-center space-x-1.5">
      <!-- Anterior -->
      <button
        @click="goTo(currentPage - 1)"
        :disabled="currentPage <= 1"
        class="px-3 py-1.5 rounded-lg border border-surface-border text-sm font-medium transition-colors disabled:opacity-40 disabled:cursor-not-allowed hover:bg-surface-light text-text-muted hover:text-white"
        aria-label="Página anterior"
      >
        Anterior
      </button>

      <!-- Números -->
      <template v-for="(p, idx) in visiblePages" :key="idx">
        <span
          v-if="p === '...'"
          class="px-2 text-text-muted text-sm"
        >...</span>
        <button
          v-else
          @click="goTo(Number(p))"
          :class="[
            'min-w-8 h-8 px-2 rounded-lg text-sm font-medium transition-all',
            p === currentPage
              ? 'bg-primary text-white shadow-glow-primary'
              : 'border border-surface-border text-text-muted hover:bg-surface-light hover:text-white'
          ]"
        >
          {{ p }}
        </button>
      </template>

      <!-- Siguiente -->
      <button
        @click="goTo(currentPage + 1)"
        :disabled="currentPage >= totalPages"
        class="px-3 py-1.5 rounded-lg border border-surface-border text-sm font-medium transition-colors disabled:opacity-40 disabled:cursor-not-allowed hover:bg-surface-light text-text-muted hover:text-white"
        aria-label="Página siguiente"
      >
        Siguiente
      </button>
    </div>
  </div>
</template>
