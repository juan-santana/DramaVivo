<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  currentTime: number
  duration: number
}>()

const emit = defineEmits<{
  (e: 'seek', time: number): void
}>()

const barRef = ref<HTMLDivElement | null>(null)

function handleSeek(e: MouseEvent) {
  if (!barRef.value || props.duration <= 0) return
  const rect = barRef.value.getBoundingClientRect()
  const clickX = e.clientX - rect.left
  const ratio = Math.max(0, Math.min(1, clickX / rect.width))
  emit('seek', ratio * props.duration)
}
</script>

<template>
  <div
    ref="barRef"
    @click="handleSeek"
    class="relative w-full h-3 flex items-center cursor-pointer group"
  >
    <!-- Background track -->
    <div class="w-full h-1 group-hover:h-2 bg-white/20 rounded-full overflow-hidden transition-all duration-150">
      <!-- Progress Fill -->
      <div
        class="h-full bg-primary relative transition-all duration-75"
        :style="{ width: `${duration > 0 ? (currentTime / duration) * 100 : 0}%` }"
      ></div>
    </div>

    <!-- Thumb Knob -->
    <div
      class="absolute w-3.5 h-3.5 bg-white rounded-full shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none -translate-x-1/2"
      :style="{ left: `${duration > 0 ? (currentTime / duration) * 100 : 0}%` }"
    ></div>
  </div>
</template>
