<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Episode } from '../../types'
import EpisodeCard from './EpisodeCard.vue'

const props = defineProps<{
  episodes: Episode[]
  currentEpisodeId?: string
}>()

const emit = defineEmits<{
  (e: 'select', episode: Episode): void
}>()

const CHUNK_SIZE = 25
const currentChunk = ref(0)

const totalChunks = computed(() => {
  return Math.ceil(props.episodes.length / CHUNK_SIZE) || 1
})

const chunkOptions = computed(() => {
  const options = []
  for (let i = 0; i < totalChunks.value; i++) {
    const start = i * CHUNK_SIZE + 1
    const end = Math.min((i + 1) * CHUNK_SIZE, props.episodes.length)
    options.push({
      index: i,
      label: `${start} - ${end}`,
    })
  }
  return options
})

const displayedEpisodes = computed(() => {
  if (props.episodes.length <= CHUNK_SIZE) return props.episodes
  const start = currentChunk.value * CHUNK_SIZE
  return props.episodes.slice(start, start + CHUNK_SIZE)
})

function onSelect(ep: Episode) {
  emit('select', ep)
}
</script>

<template>
  <div class="space-y-4">
    <!-- Header with Episode Range Switcher if more than 25 eps -->
    <div class="flex items-center justify-between pb-2 border-b border-surface-border">
      <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
        <span>Episodios</span>
        <span class="text-xs px-2 py-0.5 rounded-full bg-surface-light text-text-muted font-normal">
          {{ episodes.length }}
        </span>
      </h3>

      <div v-if="totalChunks > 1" class="flex items-center gap-1.5 overflow-x-auto no-scrollbar">
        <button
          v-for="chunk in chunkOptions"
          :key="chunk.index"
          @click="currentChunk = chunk.index"
          :class="[
            'px-2.5 py-1 rounded-lg text-xs font-medium transition-colors',
            currentChunk === chunk.index
              ? 'bg-primary text-white'
              : 'bg-surface-light text-text-muted hover:text-white'
          ]"
        >
          {{ chunk.label }}
        </button>
      </div>
    </div>

    <!-- Episodes Grid/List -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
      <EpisodeCard
        v-for="ep in displayedEpisodes"
        :key="ep.id"
        :episode="ep"
        :isActive="ep.id === currentEpisodeId"
        @click="onSelect(ep)"
      />
    </div>
  </div>
</template>
