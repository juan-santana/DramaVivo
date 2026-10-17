<script setup lang="ts">
withDefaults(
  defineProps<{
    size?: 'sm' | 'md' | 'lg'
    text?: string
    fullScreen?: boolean
  }>(),
  {
    size: 'md',
    text: '',
    fullScreen: false,
  }
)
</script>

<template>
  <div
    :class="[
      'flex flex-col items-center justify-center gap-3',
      fullScreen ? 'fixed inset-0 z-50 bg-background/80 backdrop-blur-sm' : 'py-8'
    ]"
  >
    <div
      :class="[
        'animate-spin rounded-full border-t-transparent border-primary',
        size === 'sm' ? 'w-5 h-5 border-2' : size === 'md' ? 'w-10 h-10 border-3' : 'w-16 h-16 border-4'
      ]"
      style="border-style: solid; border-color: rgba(229, 9, 20, 0.2); border-top-color: #e50914;"
    ></div>
    <p v-if="text" class="text-sm text-text-muted font-medium animate-pulse">
      {{ text }}
    </p>
  </div>
</template>
