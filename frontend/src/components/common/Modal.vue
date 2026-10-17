<script setup lang="ts">
import { watch, onMounted, onUnmounted } from 'vue'

const props = withDefaults(
  defineProps<{
    modelValue: boolean
    title?: string
    maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  }>(),
  {
    title: '',
    maxWidth: 'md',
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'close'): void
}>()

function close() {
  emit('update:modelValue', false)
  emit('close')
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && props.modelValue) {
    close()
  }
}

watch(
  () => props.modelValue,
  val => {
    if (val) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
  }
)

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = ''
})
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 overflow-y-auto bg-black/80 backdrop-blur-md flex items-center justify-center p-4"
        @click.self="close"
      >
        <div
          :class="[
            'relative w-full glass-panel rounded-2xl shadow-2xl p-6 overflow-hidden border border-surface-border animate-in fade-in zoom-in-95 duration-200',
            maxWidth === 'sm' ? 'max-w-sm' : '',
            maxWidth === 'md' ? 'max-w-md' : '',
            maxWidth === 'lg' ? 'max-w-lg' : '',
            maxWidth === 'xl' ? 'max-w-xl' : '',
            maxWidth === '2xl' ? 'max-w-2xl' : '',
          ]"
        >
          <!-- Header -->
          <div class="flex items-center justify-between pb-4 mb-4 border-b border-surface-border">
            <h3 class="text-lg font-bold text-white tracking-wide">
              {{ title }}
            </h3>
            <button
              @click="close"
              class="p-1.5 rounded-lg text-text-muted hover:text-white hover:bg-surface-light transition-colors"
              aria-label="Cerrar ventana modal"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div class="text-sm text-text-muted space-y-4">
            <slot />
          </div>

          <!-- Footer slot -->
          <div v-if="$slots.footer" class="mt-6 pt-4 border-t border-surface-border flex justify-end gap-3">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
