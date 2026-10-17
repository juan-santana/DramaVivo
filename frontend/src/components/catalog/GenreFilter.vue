<script setup lang="ts">
import type { Genre } from '../../types'

defineProps<{
  genres: Genre[]
  selectedGenre: string
}>()

const emit = defineEmits<{
  (e: 'select', genreName: string): void
}>()
</script>

<template>
  <div class="w-full overflow-x-auto no-scrollbar py-2">
    <div class="flex items-center gap-2 sm:gap-2.5 min-w-max">
      <!-- Todos Pill -->
      <button
        @click="emit('select', 'todos')"
        :class="[
          'px-4 py-2 rounded-full text-xs sm:text-sm font-semibold transition-all duration-200 border',
          selectedGenre === 'todos' || !selectedGenre
            ? 'bg-primary text-white border-primary shadow-glow-primary'
            : 'bg-surface/80 text-text-muted border-surface-border hover:bg-surface hover:text-white'
        ]"
      >
        Todos
      </button>

      <!-- Genre Pills -->
      <button
        v-for="genre in genres"
        :key="genre.id"
        @click="emit('select', genre.name)"
        :class="[
          'px-4 py-2 rounded-full text-xs sm:text-sm font-semibold transition-all duration-200 border flex items-center gap-1.5',
          selectedGenre.toLowerCase() === genre.name.toLowerCase()
            ? 'bg-primary text-white border-primary shadow-glow-primary'
            : 'bg-surface/80 text-text-muted border-surface-border hover:bg-surface hover:text-white'
        ]"
      >
        <span>{{ genre.name }}</span>
        <span
          v-if="genre.seriesCount"
          :class="[
            'text-[10px] px-1.5 py-0.2 rounded-full',
            selectedGenre.toLowerCase() === genre.name.toLowerCase()
              ? 'bg-white/20 text-white'
              : 'bg-surface-lighter text-text-dim'
          ]"
        >
          {{ genre.seriesCount }}
        </span>
      </button>
    </div>
  </div>
</template>
