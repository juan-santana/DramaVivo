<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string
    value: string | number
    change?: string
    isPositive?: boolean
    iconColor?: 'primary' | 'secondary' | 'green' | 'blue'
  }>(),
  {
    isPositive: true,
    iconColor: 'primary',
  }
)
</script>

<template>
  <div class="glass-panel p-5 sm:p-6 rounded-2xl border border-surface-border flex flex-col justify-between hover:border-surface-lighter transition-all">
    <div class="flex items-start justify-between">
      <div>
        <p class="text-xs font-medium text-text-muted uppercase tracking-wider">
          {{ title }}
        </p>
        <h3 class="text-2xl sm:text-3xl font-black text-white mt-2">
          {{ value }}
        </h3>
      </div>

      <div
        :class="[
          'p-3 rounded-xl border',
          iconColor === 'primary' ? 'bg-primary/10 border-primary/20 text-primary' : '',
          iconColor === 'secondary' ? 'bg-secondary/10 border-secondary/20 text-secondary' : '',
          iconColor === 'green' ? 'bg-green-500/10 border-green-500/20 text-green-400' : '',
          iconColor === 'blue' ? 'bg-blue-500/10 border-blue-500/20 text-blue-400' : '',
        ]"
      >
        <slot name="icon">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </slot>
      </div>
    </div>

    <div v-if="change" class="mt-4 flex items-center gap-1.5 text-xs font-semibold">
      <span :class="isPositive ? 'text-green-400' : 'text-red-400'">
        {{ change }}
      </span>
      <span class="text-text-muted font-normal">vs periodo anterior</span>
    </div>
  </div>
</template>
