<script setup lang="ts">
import Modal from '../common/Modal.vue'

withDefaults(
  defineProps<{
    modelValue: boolean
    title: string
    loading?: boolean
    submitText?: string
    cancelText?: string
    maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  }>(),
  {
    loading: false,
    submitText: 'Guardar',
    cancelText: 'Cancelar',
    maxWidth: 'md',
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'submit'): void
  (e: 'cancel'): void
}>()

function onCancel() {
  emit('update:modelValue', false)
  emit('cancel')
}

function onSubmit() {
  emit('submit')
}
</script>

<template>
  <Modal
    :modelValue="modelValue"
    :title="title"
    :maxWidth="maxWidth"
    @update:modelValue="emit('update:modelValue', $event)"
    @close="emit('cancel')"
  >
    <form @submit.prevent="onSubmit" class="space-y-4">
      <slot />

      <div class="mt-6 pt-4 border-t border-surface-border flex justify-end gap-3">
        <button
          type="button"
          @click="onCancel"
          class="px-4 py-2 rounded-xl text-xs font-semibold text-text-muted hover:text-white bg-surface-light border border-surface-border transition-colors"
        >
          {{ cancelText }}
        </button>

        <button
          type="submit"
          :disabled="loading"
          class="px-5 py-2 rounded-xl text-xs font-semibold text-white bg-primary hover:bg-primary-hover shadow-glow-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <div
            v-if="loading"
            class="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin"
          ></div>
          <span>{{ submitText }}</span>
        </button>
      </div>
    </form>
  </Modal>
</template>
