<script setup lang="ts">
import { ref, watch } from 'vue'

const props = withDefaults(
  defineProps<{
    modelValue?: string
    placeholder?: string
    debounceMs?: number
    autoFocus?: boolean
  }>(),
  {
    modelValue: '',
    placeholder: 'Buscar dramas, romances, actores...',
    debounceMs: 300,
    autoFocus: false,
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'search', value: string): void
}>()

const localQuery = ref(props.modelValue)
let timer: ReturnType<typeof setTimeout> | null = null

watch(
  () => props.modelValue,
  val => {
    if (val !== localQuery.value) {
      localQuery.value = val
    }
  }
)

function onInput() {
  emit('update:modelValue', localQuery.value)
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => {
    emit('search', localQuery.value)
  }, props.debounceMs)
}

function clear() {
  localQuery.value = ''
  emit('update:modelValue', '')
  emit('search', '')
}
</script>

<template>
  <div class="relative w-full">
    <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-text-muted">
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>

    <input
      type="text"
      v-model="localQuery"
      @input="onInput"
      :placeholder="placeholder"
      :autofocus="autoFocus"
      class="w-full pl-11 pr-10 py-3 bg-surface/90 hover:bg-surface border border-surface-border rounded-xl text-white placeholder-text-muted/60 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all text-sm"
    />

    <button
      v-if="localQuery"
      @click="clear"
      class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-text-muted hover:text-white transition-colors"
      aria-label="Borrar búsqueda"
    >
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
  </div>
</template>
