<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isVisible = ref(false)

onMounted(() => {
  const consent = localStorage.getItem('dramaapp_cookie_consent')
  if (!consent) {
    // Show banner after short delay
    setTimeout(() => {
      isVisible.value = true
    }, 1000)
  }
})

function acceptAll() {
  localStorage.setItem('dramaapp_cookie_consent', 'accepted')
  isVisible.value = false
}

function rejectNonEssential() {
  localStorage.setItem('dramaapp_cookie_consent', 'essential_only')
  isVisible.value = false
}
</script>

<template>
  <Transition
    enter-active-class="transform ease-out duration-300 transition"
    enter-from-class="translate-y-full opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="translate-y-full opacity-0"
  >
    <div
      v-if="isVisible"
      class="fixed bottom-4 inset-x-4 sm:left-auto sm:right-4 sm:max-w-md z-50 glass-panel border border-surface-border p-5 rounded-2xl shadow-2xl"
    >
      <div class="flex items-start gap-3 mb-3">
        <div class="p-2 rounded-lg bg-primary/10 text-primary shrink-0">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <div>
          <h4 class="text-sm font-semibold text-white">Privacidad y Cookies</h4>
          <p class="text-xs text-text-muted mt-1 leading-relaxed">
            Utilizamos cookies esenciales y analíticas para optimizar tu experiencia en streaming vertical y recordar tu historial de reproducción.
            Consulta nuestra
            <router-link to="/cookies" class="text-secondary hover:underline">
              Política de Cookies
            </router-link>.
          </p>
        </div>
      </div>

      <div class="flex items-center justify-end gap-2.5 pt-2">
        <button
          @click="rejectNonEssential"
          class="px-3.5 py-1.5 text-xs font-medium text-text-muted hover:text-white rounded-lg hover:bg-surface-light border border-surface-border transition-colors"
        >
          Solo esenciales
        </button>
        <button
          @click="acceptAll"
          class="px-4 py-1.5 text-xs font-semibold text-white bg-primary hover:bg-primary-hover rounded-lg shadow-glow-primary transition-all"
        >
          Aceptar todas
        </button>
      </div>
    </div>
  </Transition>
</template>
