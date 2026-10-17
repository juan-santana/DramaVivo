<script setup lang="ts" generic="T extends Record<string, any>">
import { ref, computed } from 'vue'
import Pagination from '../common/Pagination.vue'
import LoadingSpinner from '../common/LoadingSpinner.vue'

export interface TableColumn {
  key: string
  label: string
  sortable?: boolean
  align?: 'left' | 'center' | 'right'
}

const props = withDefaults(
  defineProps<{
    columns: TableColumn[]
    data: T[]
    loading?: boolean
    searchable?: boolean
    searchPlaceholder?: string
    pageSize?: number
    emptyText?: string
  }>(),
  {
    loading: false,
    searchable: true,
    searchPlaceholder: 'Buscar registros...',
    pageSize: 10,
    emptyText: 'No se encontraron registros.',
  }
)

const searchQuery = ref('')
const sortKey = ref<string>('')
const sortOrder = ref<'asc' | 'desc'>('asc')
const currentPage = ref(1)

function setSort(key: string) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

const filteredData = computed(() => {
  let list = [...props.data]

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase().trim()
    list = list.filter(item =>
      Object.values(item).some(val =>
        String(val ?? '').toLowerCase().includes(q)
      )
    )
  }

  if (sortKey.value) {
    const key = sortKey.value
    const order = sortOrder.value === 'asc' ? 1 : -1
    list.sort((a, b) => {
      const valA = a[key]
      const valB = b[key]
      if (valA === valB) return 0
      if (valA == null) return 1
      if (valB == null) return -1
      return valA > valB ? order : -order
    })
  }

  return list
})

const totalPages = computed(() => Math.ceil(filteredData.value.length / props.pageSize) || 1)

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * props.pageSize
  return filteredData.value.slice(start, start + props.pageSize)
})

function onPageChange(page: number) {
  currentPage.value = page
}
</script>

<template>
  <div class="glass-panel rounded-2xl border border-surface-border overflow-hidden">
    <!-- Table Header Toolbar -->
    <div v-if="searchable || $slots.actions" class="p-4 sm:p-5 border-b border-surface-border flex flex-col sm:flex-row items-center justify-between gap-4">
      <div v-if="searchable" class="relative w-full sm:w-72">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-text-muted">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="searchPlaceholder"
          class="w-full pl-9 pr-4 py-2 bg-surface border border-surface-border rounded-xl text-xs text-white placeholder-text-muted/60 focus:outline-none focus:border-primary"
        />
      </div>

      <div class="flex items-center gap-3 w-full sm:w-auto justify-end">
        <slot name="actions" />
      </div>
    </div>

    <!-- Table element -->
    <div class="overflow-x-auto no-scrollbar">
      <table class="w-full text-left text-sm text-text-muted">
        <thead class="bg-surface-light/60 text-xs uppercase font-semibold tracking-wider text-text-muted border-b border-surface-border">
          <tr>
            <th
              v-for="col in columns"
              :key="col.key"
              @click="col.sortable ? setSort(col.key) : null"
              :class="[
                'px-5 py-3.5',
                col.sortable ? 'cursor-pointer hover:text-white select-none' : '',
                col.align === 'center' ? 'text-center' : col.align === 'right' ? 'text-right' : 'text-left'
              ]"
            >
              <div class="inline-flex items-center gap-1.5">
                <span>{{ col.label }}</span>
                <span v-if="col.sortable" class="text-text-dim">
                  <span v-if="sortKey === col.key && sortOrder === 'asc'">▲</span>
                  <span v-else-if="sortKey === col.key && sortOrder === 'desc'">▼</span>
                  <span v-else>⇅</span>
                </span>
              </div>
            </th>
            <th v-if="$slots.rowActions" class="px-5 py-3.5 text-right">
              Acciones
            </th>
          </tr>
        </thead>

        <tbody class="divide-y divide-surface-border">
          <tr v-if="loading">
            <td :colspan="columns.length + ($slots.rowActions ? 1 : 0)" class="py-12 text-center">
              <LoadingSpinner size="md" text="Cargando datos..." />
            </td>
          </tr>

          <tr v-else-if="paginatedData.length === 0">
            <td :colspan="columns.length + ($slots.rowActions ? 1 : 0)" class="py-12 text-center text-xs text-text-muted">
              {{ emptyText }}
            </td>
          </tr>

          <tr
            v-else
            v-for="(item, idx) in paginatedData"
            :key="idx"
            class="hover:bg-surface-light/40 transition-colors"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              :class="[
                'px-5 py-4 text-xs font-medium',
                col.align === 'center' ? 'text-center' : col.align === 'right' ? 'text-right' : 'text-left'
              ]"
            >
              <slot :name="col.key" :item="item" :value="item[col.key]">
                {{ item[col.key] }}
              </slot>
            </td>

            <td v-if="$slots.rowActions" class="px-5 py-4 text-right text-xs">
              <slot name="rowActions" :item="item" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Table Footer with Pagination -->
    <div v-if="totalPages > 1" class="p-4 border-t border-surface-border">
      <Pagination
        :currentPage="currentPage"
        :totalPages="totalPages"
        :totalItems="filteredData.length"
        @change="onPageChange"
      />
    </div>
  </div>
</template>
