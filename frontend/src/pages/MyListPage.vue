<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useHead } from '@unhead/vue'
import { useFavoritesStore } from '../stores/favorites'
import { useI18n } from '../i18n'

const router = useRouter()
const favoritesStore = useFavoritesStore()
const { t } = useI18n()

useHead({
  title: 'Mi Lista - DramaVivo',
  meta: [
    { name: 'description', content: 'Tus series y episodios favoritos guardados localmente en DramaVivo.' }
  ]
})

const activeTab = ref<'lista' | 'continuar' | 'historial'>('lista')

const continueWatchingList = computed(() => {
  return favoritesStore.history.filter(h => h.progressSeconds > 5 && h.progressSeconds < h.durationSeconds - 5)
})

function formatProgress(seconds: number) {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m}:${s < 10 ? '0' : ''}${s}`
}

function removeFav(seriesId: string) {
  favoritesStore.removeFavorite(seriesId)
}

function playSeries(seriesId: string) {
  router.push(`/serie/${seriesId}`)
}

function resumeEpisode(seriesId: string, episodeId: string) {
  router.push(`/reproducir/${seriesId}/${episodeId}`)
}

function clearAllHistory() {
  if (confirm('¿Estás seguro de que deseas borrar tu historial de reproducción?')) {
    favoritesStore.clearHistory()
  }
}
</script>

<template>
  <div class="min-h-screen pb-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
      <!-- Header Banner -->
      <div class="glass-panel p-6 sm:p-8 rounded-3xl border border-surface-border flex flex-col sm:flex-row items-center justify-between gap-6 relative overflow-hidden">
        <div class="absolute -top-24 -left-24 w-64 h-64 bg-primary/15 rounded-full blur-3xl pointer-events-none"></div>
        <div class="absolute -bottom-24 -right-24 w-64 h-64 bg-secondary/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="flex items-center gap-4 z-10">
          <div class="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl bg-gradient-to-tr from-rose-500 via-amber-400 to-purple-600 p-0.5 shadow-glow-primary shrink-0">
            <div class="w-full h-full bg-[#12121a] rounded-[14px] flex items-center justify-center text-secondary">
              <svg class="w-7 h-7 sm:w-8 sm:h-8 fill-current" viewBox="0 0 24 24">
                <path d="M17 3H7c-1.1 0-2 .9-2 2v16l7-3 7 3V5c0-1.1-.9-2-2-2z" />
              </svg>
            </div>
          </div>
          <div>
            <h1 class="text-2xl sm:text-3xl font-black text-white flex items-center gap-2">
              Mi Lista
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-secondary/20 text-secondary border border-secondary/30 font-mono font-bold">
                {{ favoritesStore.favorites.length }} Guardados
              </span>
            </h1>
            <p class="text-xs sm:text-sm text-text-muted mt-1">
              Colección personal sincronizada localmente en tu dispositivo. Accede sin registrarte.
            </p>
          </div>
        </div>

        <div class="flex items-center gap-3 z-10">
          <router-link
            to="/catalogo"
            class="px-4 py-2.5 rounded-xl bg-primary hover:bg-primary-hover text-white text-xs font-bold shadow-glow-primary transition-all flex items-center gap-2"
          >
            <span>+ Explorar Catálogo</span>
          </router-link>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex items-center justify-between border-b border-surface-border">
        <div class="flex items-center gap-4 sm:gap-8">
          <button
            @click="activeTab = 'lista'"
            :class="[
              'pb-4 text-sm font-bold transition-all relative flex items-center gap-2',
              activeTab === 'lista'
                ? 'text-white'
                : 'text-text-muted hover:text-white'
            ]"
          >
            <span>Mi Lista Guardada</span>
            <span
              v-if="favoritesStore.favorites.length > 0"
              class="px-2 py-0.5 text-xs rounded-full bg-secondary/20 text-secondary font-mono font-bold"
            >
              {{ favoritesStore.favorites.length }}
            </span>
            <div
              v-if="activeTab === 'lista'"
              class="absolute bottom-0 inset-x-0 h-0.5 bg-secondary shadow-glow-gold"
            ></div>
          </button>

          <button
            @click="activeTab = 'continuar'"
            :class="[
              'pb-4 text-sm font-bold transition-all relative flex items-center gap-2',
              activeTab === 'continuar'
                ? 'text-white'
                : 'text-text-muted hover:text-white'
            ]"
          >
            <span>Continuar Viendo</span>
            <span
              v-if="continueWatchingList.length > 0"
              class="px-2 py-0.5 text-xs rounded-full bg-primary/20 text-primary font-mono font-bold"
            >
              {{ continueWatchingList.length }}
            </span>
            <div
              v-if="activeTab === 'continuar'"
              class="absolute bottom-0 inset-x-0 h-0.5 bg-primary shadow-glow-primary"
            ></div>
          </button>

          <button
            @click="activeTab = 'historial'"
            :class="[
              'pb-4 text-sm font-bold transition-all relative flex items-center gap-2',
              activeTab === 'historial'
                ? 'text-white'
                : 'text-text-muted hover:text-white'
            ]"
          >
            <span>Historial Reciente</span>
            <span
              v-if="favoritesStore.history.length > 0"
              class="px-2 py-0.5 text-xs rounded-full bg-surface-lighter text-text-muted font-mono font-bold"
            >
              {{ favoritesStore.history.length }}
            </span>
            <div
              v-if="activeTab === 'historial'"
              class="absolute bottom-0 inset-x-0 h-0.5 bg-white"
            ></div>
          </button>
        </div>

        <button
          v-if="activeTab === 'historial' && favoritesStore.history.length > 0"
          @click="clearAllHistory"
          class="text-xs text-red-400 hover:text-red-300 pb-4 transition-colors flex items-center gap-1"
        >
          <span>Vaciar historial</span>
        </button>
      </div>

      <!-- Tab Content: Mi Lista Guardada -->
      <div v-if="activeTab === 'lista'">
        <!-- Empty State -->
        <div
          v-if="favoritesStore.favorites.length === 0"
          class="glass-panel p-12 sm:p-16 rounded-3xl border border-surface-border text-center space-y-4 max-w-lg mx-auto"
        >
          <div class="w-16 h-16 rounded-full bg-surface-light flex items-center justify-center mx-auto text-text-muted text-2xl">
            🔖
          </div>
          <h3 class="text-lg font-bold text-white">Tu lista está vacía</h3>
          <p class="text-xs sm:text-sm text-text-muted">
            Agrega dramas haciendo clic en el botón <strong>"+ Mi Lista"</strong> en la portada de cualquier serie para verlos más tarde.
          </p>
          <div class="pt-2">
            <router-link
              to="/catalogo"
              class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary hover:bg-primary-hover text-white text-xs font-bold shadow-glow-primary transition-all"
            >
              Explorar Catálogo de Dramas
            </router-link>
          </div>
        </div>

        <!-- Series Grid -->
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 sm:gap-6">
          <div
            v-for="item in favoritesStore.favorites"
            :key="item.seriesId"
            class="group relative flex flex-col rounded-2xl overflow-hidden bg-surface border border-surface-border hover:border-primary/50 transition-all duration-300 hover:shadow-2xl hover:-translate-y-1"
          >
            <!-- Poster Image Container -->
            <div class="aspect-[9/14] w-full overflow-hidden bg-surface-dark relative">
              <img
                :src="item.posterUrl"
                :alt="item.seriesTitle"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                loading="lazy"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent opacity-80 group-hover:opacity-40 transition-opacity"></div>

              <!-- Top Action: Remove Button -->
              <button
                @click.stop="removeFav(item.seriesId)"
                class="absolute top-2 right-2 w-8 h-8 rounded-full bg-black/70 hover:bg-red-600 text-white/80 hover:text-white flex items-center justify-center backdrop-blur-md transition-all shadow-md z-20"
                title="Quitar de Mi Lista"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>

              <!-- Play Overlay Button -->
              <button
                @click="playSeries(item.seriesId)"
                class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity z-10"
              >
                <div class="w-12 h-12 rounded-full bg-primary/90 text-white flex items-center justify-center shadow-glow-primary transform scale-90 group-hover:scale-100 transition-transform">
                  <svg class="w-6 h-6 fill-current translate-x-0.5" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                </div>
              </button>

              <!-- Episode Count Badge -->
              <div class="absolute bottom-2 left-2 px-2 py-0.5 rounded-md bg-black/70 text-secondary text-[10px] font-bold font-mono backdrop-blur-sm border border-secondary/30">
                {{ item.totalEpisodes }} Eps
              </div>
            </div>

            <!-- Meta Details -->
            <div class="p-3 flex-1 flex flex-col justify-between">
              <div>
                <h4 class="text-xs sm:text-sm font-bold text-white line-clamp-1 group-hover:text-primary transition-colors" :title="item.seriesTitle">
                  {{ item.seriesTitle }}
                </h4>
                <div class="flex flex-wrap gap-1 mt-1">
                  <span
                    v-for="g in (item.genres || []).slice(0, 2)"
                    :key="g"
                    class="text-[9px] px-1.5 py-0.2 rounded bg-surface-lighter text-text-muted"
                  >
                    {{ g }}
                  </span>
                </div>
              </div>

              <button
                @click="playSeries(item.seriesId)"
                class="mt-3 w-full py-1.5 rounded-lg bg-surface-light hover:bg-primary text-text-muted hover:text-white text-[11px] font-bold transition-all text-center"
              >
                Ver Ahora
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab Content: Continuar Viendo -->
      <div v-else-if="activeTab === 'continuar'">
        <div
          v-if="continueWatchingList.length === 0"
          class="glass-panel p-12 rounded-3xl border border-surface-border text-center space-y-3 max-w-lg mx-auto"
        >
          <div class="w-14 h-14 rounded-full bg-surface-light flex items-center justify-center mx-auto text-text-muted text-xl">
            ⏱️
          </div>
          <h3 class="text-base font-bold text-white">No tienes episodios pendientes</h3>
          <p class="text-xs text-text-muted">
            Cuando comiences a ver una serie, guardaremos automáticamente el segundo exacto donde te quedaste.
          </p>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          <div
            v-for="item in continueWatchingList"
            :key="item.episodeId"
            @click="resumeEpisode(item.seriesId, item.episodeId)"
            class="group cursor-pointer glass-panel p-4 rounded-2xl border border-surface-border hover:border-primary/50 transition-all flex gap-4 items-center"
          >
            <div class="w-20 sm:w-24 aspect-[9/14] rounded-xl overflow-hidden bg-surface-dark relative shrink-0">
              <img :src="item.posterUrl" :alt="item.seriesTitle" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <svg class="w-8 h-8 text-white fill-current" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z" />
                </svg>
              </div>
            </div>

            <div class="flex-1 min-w-0 space-y-2">
              <div>
                <span class="text-[10px] font-bold text-primary font-mono uppercase tracking-wider block">
                  Capítulo {{ item.episodeNumber }}
                </span>
                <h4 class="text-xs sm:text-sm font-bold text-white truncate" :title="item.seriesTitle">
                  {{ item.seriesTitle }}
                </h4>
              </div>

              <!-- Progress bar -->
              <div class="space-y-1">
                <div class="w-full h-1.5 rounded-full bg-surface-lighter overflow-hidden">
                  <div
                    class="h-full bg-primary rounded-full shadow-glow-primary"
                    :style="{ width: `${(item.progressSeconds / item.durationSeconds) * 100}%` }"
                  ></div>
                </div>
                <div class="flex items-center justify-between text-[10px] text-text-muted font-mono">
                  <span>{{ formatProgress(item.progressSeconds) }}</span>
                  <span>{{ formatProgress(item.durationSeconds) }}</span>
                </div>
              </div>

              <button
                class="px-3 py-1 rounded-lg bg-primary/20 hover:bg-primary text-primary hover:text-white text-xs font-semibold transition-colors"
              >
                Reanudar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab Content: Historial Completo -->
      <div v-else-if="activeTab === 'historial'">
        <div
          v-if="favoritesStore.history.length === 0"
          class="glass-panel p-12 rounded-3xl border border-surface-border text-center space-y-3 max-w-lg mx-auto"
        >
          <div class="w-14 h-14 rounded-full bg-surface-light flex items-center justify-center mx-auto text-text-muted text-xl">
            📜
          </div>
          <h3 class="text-base font-bold text-white">Historial vacío</h3>
          <p class="text-xs text-text-muted">Los episodios que reproduzcas aparecerán en esta lista cronológica.</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="item in favoritesStore.history"
            :key="item.episodeId + item.lastWatchedAt"
            @click="resumeEpisode(item.seriesId, item.episodeId)"
            class="group cursor-pointer p-3 sm:p-4 rounded-xl bg-surface/60 border border-surface-border hover:border-primary/40 transition-all flex items-center justify-between gap-4"
          >
            <div class="flex items-center gap-3 sm:gap-4 min-w-0">
              <div class="w-12 h-16 rounded-lg overflow-hidden bg-surface-dark shrink-0">
                <img :src="item.posterUrl" :alt="item.seriesTitle" class="w-full h-full object-cover" />
              </div>
              <div class="min-w-0">
                <h4 class="text-xs sm:text-sm font-bold text-white truncate">{{ item.seriesTitle }}</h4>
                <p class="text-[11px] text-text-muted">
                  Capítulo {{ item.episodeNumber }} • Visto hace un momento
                </p>
              </div>
            </div>

            <div class="flex items-center gap-3 shrink-0">
              <button
                class="px-3 py-1.5 rounded-lg bg-surface-light hover:bg-primary text-text-muted hover:text-white text-xs font-bold transition-colors"
              >
                Ver de nuevo
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
