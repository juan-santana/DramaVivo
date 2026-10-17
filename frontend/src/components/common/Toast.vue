<script setup lang="ts">
import { useToast } from '../../composables/useToast'

const { toasts, dismiss } = useToast()
</script>

<template>
  <div class="fixed top-5 right-5 z-50 flex flex-col gap-3 max-w-sm w-full pointer-events-none">
    <TransitionGroup
      enter-active-class="transform ease-out duration-300 transition"
      enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
      enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'pointer-events-auto flex items-start gap-3 p-4 rounded-xl shadow-2xl border backdrop-blur-md transition-all',
          toast.type === 'success' ? 'bg-[#0f2e1b]/90 border-green-500/40 text-green-200' : '',
          toast.type === 'error' ? 'bg-[#3b1219]/90 border-red-500/40 text-red-200' : '',
          toast.type === 'warning' ? 'bg-[#3b2d0d]/90 border-yellow-500/40 text-yellow-200' : '',
          toast.type === 'info' || !toast.type ? 'bg-surface/90 border-surface-border text-white' : '',
        ]"
      >
        <!-- Icon -->
        <div class="shrink-0 mt-0.5">
          <svg v-if="toast.type === 'success'" class="w-5 h-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else-if="toast.type === 'error'" class="w-5 h-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <svg v-else-if="toast.type === 'warning'" class="w-5 h-5 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <svg v-else class="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>

        <!-- Content -->
        <div class="flex-1 min-w-0">
          <h4 v-if="toast.title" class="text-sm font-semibold text-white mb-0.5">
            {{ toast.title }}
          </h4>
          <p class="text-xs opacity-90 leading-relaxed">
            {{ toast.message }}
          </p>
        </div>

        <!-- Dismiss button -->
        <button
          @click="dismiss(toast.id)"
          class="shrink-0 p-1 rounded-md opacity-60 hover:opacity-100 transition-opacity"
          aria-label="Cerrar notificación"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>
