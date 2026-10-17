<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useHead } from '@unhead/vue'
import { useFavoritesStore } from '../stores/favorites'

const router = useRouter()
const favoritesStore = useFavoritesStore()

useHead({
  title: 'Mi Perfil y Lista - DramaApp',
})

const activeTab = ref<'continuar' | 'favoritos' | 'historial'>('continuar')

const formatProgress = (seconds: number) => {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m}:${s < 10 ? '0' : ''}${s}`
}

function resumeWatching(seriesId: string, episodeId: string) {
  router.push(`/reproducir/${seriesId}/${episodeId}`)
}

function removeFav(seriesId: string) {
  favoritesStore.removeFavorite(seriesId)
}

function clearAllHistory() {
  if (confirm('¿Estás seguro de que deseas borrar todo tu historial de reproducción?')) {
    favoritesStore.clearHistory()
  }
}

const continueWatchingList = computed(() => {
  return favoritesStore.history.filter(h => h.progressSeconds > 5 && h.progressSeconds < h.durationSeconds - 5)
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
    <!-- Header banner -->
    <div class="glass-panel p-6 sm:p-8 rounded-3xl border border-surface-border flex flex-col sm:flex-row items-center justify-between gap-6">
      <div class="flex items-center gap-4">
        <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-primary to-primary-light flex items-center justify-center text-white text-2xl font-black shadow-glow-primary">
          <svg class="w-8 h-8 fill-current" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z" />
          </svg>
        </div>
        <div>
          <h1 class="text-2xl sm:text-3xl font-black text-white">Mi Espacio DramaApp</h1>
          <p class="text-xs sm:text-sm text-text-muted mt-0.5">Tus series guardadas y capítulos en progreso (almacenamiento local seguro)</p>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <span class="px-3 py-1.5 rounded-xl bg-surface-light border border-surface-border text-xs text-text-muted">
          {{ favoritesStore.favorites.length }} Favoritos
        </span>
        <span class="px-3 py-1.5 rounded-xl bg-surface-light border border-surface-border text-xs text-text-muted">
          {{ favoritesStore.history.length }} En Historial
        </span>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="flex items-center justify-between border-b border-surface-border">
      <div class="flex items-center gap-4 sm:gap-8">
        <button
          @click="activeTab = 'continuar'"
          :class="[
            'pb-4 text-sm font-bold transition-all relative',
            activeTab === 'continuar'
              ? 'text-white'
              : 'text-text-muted hover:text-white'
          ]"
        >
          <span>Continuar Viendo</span>
          <span v-if="continueWatchingList.length > 0" class="ml-1.5 text-xs text-primary font-mono font-bold">
            ({{ continueWatchingList.length }})
          </span>
          <div
            v-if="activeTab === 'continuar'"
            class="absolute bottom-0 inset-x-0 h-0.5 bg-primary shadow-glow-primary"
          ></div>
        </button>

        <button
          @click="activeTab = 'favoritos'"
          :class="[
            'pb-4 text-sm font-bold transition-all relative',
            activeTab === 'favoritos'
              ? 'text-white'
              : 'text-text-muted hover:text-white'
          ]"
        >
          <span>Mis Favoritos</span>
          <span v-if="favoritesStore.favorites.length > 0" class="ml-1.5 text-xs text-secondary font-mono font-bold">
            ({{ favoritesStore.favorites.length }})
          </span>
          <div
            v-if="activeTab === 'favoritos'"
            class="absolute bottom-0 inset-x-0 h-0.5 bg-secondary shadow-glow-secondary"
          ></div>
        </button>

        <button
          @click="activeTab = 'historial'"
          :class="[
            'pb-4 text-sm font-bold transition-all relative',
            activeTab === 'historial'
              ? 'text-white'
              : 'text-text-muted hover:text-white'
          ]"
        >
          <span>Historial Completo</span>
          <div
            v-if="activeTab === 'historial'"
            class="absolute bottom-0 inset-x-0 h-0.5 bg-primary shadow-glow-primary"
          ></div>
        </button>
      </div>

      <button
        v-if="activeTab === 'historial' && favoritesStore.history.length > 0"
        @click="clearAllHistory"
        class="text-xs text-red-400 hover:text-red-300 font-semibold mb-4 transition-colors"
      >
        Vaciar historial
      </button>
    </div>

    <!-- Tab 1: Continuar Viendo -->
    <div v-if="activeTab === 'continuar'">
      <div v-if="continueWatchingList.length === 0" class="py-16 text-center space-y-3">
        <div class="w-12 h-12 rounded-full bg-surface-light mx-auto flex items-center justify-center text-text-dim text-xl">
          🎬
        </div>
        <h3 class="text-base font-bold text-white">No tienes episodios pendientes</h3>
        <p class="text-xs text-text-muted max-w-sm mx-auto">Cuando comiences a reproducir un microdrama, guardaremos tu avance exacto aquí.</p>
        <router-link
          to="/catalogo"
          class="inline-block mt-2 px-5 py-2.5 rounded-xl bg-primary text-white text-xs font-semibold shadow-glow-primary"
        >
          Explorar microdramas
        </router-link>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="item in continueWatchingList"
          :key="item.seriesId"
          class="glass-panel rounded-2xl border border-surface-border overflow-hidden p-3.5 flex items-center gap-4 hover:border-surface-lighter transition-all"
        >
          <div class="w-20 aspect-[2/3] rounded-xl overflow-hidden bg-surface-light shrink-0 relative">
            <img :src="item.posterUrl" :alt="item.seriesTitle" class="w-full h-full object-cover" />
          </div>

          <div class="flex-1 min-w-0 space-y-1.5">
            <span class="text-[10px] font-mono text-primary font-bold">
              CAPÍTULO {{ item.episodeNumber }}
            </span>
            <h4 class="text-sm font-bold text-white truncate">
              {{ item.seriesTitle }}
            </h4>

            <!-- Progress Bar -->
            <div class="space-y-1">
              <div class="w-full h-1.5 bg-surface-light rounded-full overflow-hidden">
                <div
                  class="h-full bg-primary"
                  :style="{ width: `${(item.progressSeconds / item.durationSeconds) * 100}%` }"
                ></div>
              </div>
              <p class="text-[10px] text-text-muted font-mono">
                {{ formatProgress(item.progressSeconds) }} / {{ formatProgress(item.durationSeconds) }}
              </p>
            </div>

            <button
              @click="resumeWatching(item.seriesId, item.episodeId)"
              class="w-full mt-2 py-1.5 rounded-lg bg-primary hover:bg-primary-hover text-white text-xs font-semibold shadow-glow-primary transition-all flex items-center justify-center gap-1.5"
            >
              <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
              <span>Reanudar</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab 2: Mis Favoritos -->
    <div v-else-if="activeTab === 'favoritos'">
      <div v-if="favoritesStore.favorites.length === 0" class="py-16 text-center space-y-3">
        <div class="w-12 h-12 rounded-full bg-surface-light mx-auto flex items-center justify-center text-text-dim text-xl">
          ❤️
        </div>
        <h3 class="text-base font-bold text-white">Tu lista de favoritos está vacía</h3>
        <p class="text-xs text-text-muted max-w-sm mx-auto">Marca series con el ícono de corazón para tenerlas siempre a mano en cualquier momento.</p>
        <router-link
          to="/catalogo"
          class="inline-block mt-2 px-5 py-2.5 rounded-xl bg-primary text-white text-xs font-semibold shadow-glow-primary"
        >
          Descubrir series
        </router-link>
      </div>

      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        <div
          v-for="fav in favoritesStore.favorites"
          :key="fav.seriesId"
          class="relative group rounded-2xl overflow-hidden glass-panel border border-surface-border flex flex-col justify-between"
        >
          <router-link :to="`/serie/${fav.seriesId}`" class="block aspect-[2/3] overflow-hidden bg-surface-light">
            <img :src="fav.posterUrl" :alt="fav.seriesTitle" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
          </router-link>

          <button
            @click="removeFav(fav.seriesId)"
            class="absolute top-2 right-2 p-1.5 rounded-full bg-black/70 text-red-400 hover:text-red-300 backdrop-blur-md"
            title="Quitar de favoritos"
          >
            ✕
          </button>

          <div class="p-3">
            <h4 class="text-xs font-bold text-white truncate">{{ fav.seriesTitle }}</h4>
            <p class="text-[11px] text-text-muted">{{ fav.totalEpisodes }} capítulos</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab 3: Historial Completo -->
    <div v-else-if="activeTab === 'historial'">
      <div v-if="favoritesStore.history.length === 0" class="py-16 text-center space-y-3">
        <div class="w-12 h-12 rounded-full bg-surface-light mx-auto flex items-center justify-center text-text-dim text-xl">
          ⏱️
        </div>
        <h3 class="text-base font-bold text-white">No hay reproducciones recientes</h3>
        <p class="text-xs text-text-muted">Los capítulos que veas se registrarán automáticamente aquí.</p>
      </div>

      <div v-else class="space-y-3 max-w-3xl">
        <div
          v-for="item in favoritesStore.history"
          :key="`${item.seriesId}-${item.episodeId}`"
          class="glass-panel p-3.5 rounded-xl border border-surface-border flex items-center justify-between gap-4"
        >
          <div class="flex items-center gap-3">
            <img :src="item.posterUrl" :alt="item.seriesTitle" class="w-12 aspect-[2/3] rounded-lg object-cover" />
            <div>
              <h4 class="text-xs sm:text-sm font-bold text-white">{{ item.seriesTitle }}</h4>
              <p class="text-xs text-text-muted font-mono">
                Capítulo {{ item.episodeNumber }} • {{ new Date(item.lastWatchedAt).toLocaleDateString('es-ES') }}
              </p>
            </div>
          </div>

          <button
            @click="resumeWatching(item.seriesId, item.episodeId)"
            class="px-3 py-1.5 rounded-lg bg-surface-light hover:bg-surface-lighter text-white text-xs font-semibold border border-surface-border"
          >
            Ver
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
