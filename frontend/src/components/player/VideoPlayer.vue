<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue'
import videojs from 'video.js'
import type { Episode, EpisodeSubtitle } from '../../types'
import ProgressBar from './ProgressBar.vue'

const props = withDefaults(
  defineProps<{
    episode: Episode
    seriesTitle?: string
    initialTime?: number
    autoplay?: boolean
  }>(),
  {
    seriesTitle: '',
    initialTime: 0,
    autoplay: false,
  }
)

const emit = defineEmits<{
  (e: 'timeupdate', time: number, duration: number): void
  (e: 'ended'): void
  (e: 'next'): void
  (e: 'prev'): void
}>()

const videoContainerRef = ref<HTMLDivElement | null>(null)
const videoElementRef = ref<HTMLVideoElement | null>(null)
let player: any = null

const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(props.episode.duration || 0)
const isMuted = ref(false)
const volume = ref(1)
const isFullscreen = ref(false)
const showControls = ref(true)
const hasError = ref(false)
const errorMessage = ref('')
const activeSubtitle = ref<string>('es')
const activeAudio = ref<string>('es')
const showSubtitleMenu = ref(false)
const showAudioMenu = ref(false)
let hideControlsTimer: ReturnType<typeof setTimeout> | null = null

// Check if episode is hosted on ReelShort embed
const isReelShort = computed(() => {
  return !!props.episode.videoUrl && props.episode.videoUrl.includes('reelshort.com/es/embed')
})

const isExternalEmbed = computed(() => isReelShort.value)

const formatTime = (seconds: number) => {
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${m}:${s < 10 ? '0' : ''}${s}`
}

const formattedCurrentTime = computed(() => formatTime(currentTime.value))
const formattedDuration = computed(() => formatTime(duration.value))

function resetHideTimer() {
  showControls.value = true
  if (hideControlsTimer) clearTimeout(hideControlsTimer)
  if (isPlaying.value) {
    hideControlsTimer = setTimeout(() => {
      showControls.value = false
      showSubtitleMenu.value = false
      showAudioMenu.value = false
    }, 3500)
  }
}

function initPlayer() {
  if (isExternalEmbed.value || !videoElementRef.value) return

  hasError.value = false
  errorMessage.value = ''

  player = videojs(videoElementRef.value, {
    controls: false, // Custom cinematic overlay
    autoplay: false, // Explicit requirement: NO autoplay with sound
    muted: false,
    preload: 'auto',
    responsive: false,
    fluid: false,
    sources: [
      {
        src: props.episode.videoUrl,
        type: props.episode.videoUrl.endsWith('.m3u8') ? 'application/x-mpegURL' : 'video/mp4',
      },
    ],
  })

  player.on('ready', () => {
    if (props.initialTime > 0 && player) {
      player.currentTime(props.initialTime)
    }
  })

  player.on('loadedmetadata', () => {
    // 1. Force Spanish Audio Track
    try {
      const audioTracks = player.audioTracks?.()
      if (audioTracks && audioTracks.length > 1) {
        for (let i = 0; i < audioTracks.length; i++) {
          const track = audioTracks[i]
          const isSpanish = track.language?.toLowerCase().startsWith('es') ||
                            track.label?.toLowerCase().includes('español')
          track.enabled = isSpanish
          if (isSpanish) {
            activeAudio.value = 'es'
          }
        }
      }
    } catch (e) {
      console.warn('Audio tracks check:', e)
    }

    // 2. Force Spanish Subtitle Track to showing
    try {
      const textTracks = player.textTracks?.()
      if (textTracks && textTracks.length > 0) {
        for (let i = 0; i < textTracks.length; i++) {
          const track = textTracks[i]
          const isSpanish = track.language?.toLowerCase().startsWith('es') ||
                            track.label?.toLowerCase().includes('español')
          if (isSpanish) {
            track.mode = 'showing'
            activeSubtitle.value = 'es'
            break
          }
        }
      }
    } catch (e) {
      console.warn('Text tracks check:', e)
    }
  })

  player.on('play', () => {
    isPlaying.value = true
    resetHideTimer()
  })

  player.on('pause', () => {
    isPlaying.value = false
    showControls.value = true
  })

  player.on('timeupdate', () => {
    if (player) {
      const cur = player.currentTime() || 0
      const dur = player.duration() || props.episode.duration || 0
      currentTime.value = cur
      duration.value = dur
      emit('timeupdate', cur, dur)
    }
  })

  player.on('ended', () => {
    isPlaying.value = false
    showControls.value = true
    emit('ended')
  })

  player.on('error', () => {
    hasError.value = true
    errorMessage.value = 'No se pudo reproducir este video. Verifica tu conexión.'
  })

  // Setup tracks
  setupSubtitles(props.episode.subtitles)
}

function setupSubtitles(subtitles?: EpisodeSubtitle[]) {
  if (!player) return

  const tracks = player.remoteTextTracks()
  if (tracks) {
    for (let i = tracks.length - 1; i >= 0; i--) {
      player.removeRemoteTextTrack(tracks[i])
    }
  }

  if (subtitles && subtitles.length > 0) {
    subtitles.forEach(sub => {
      if (sub.src) {
        player?.addRemoteTextTrack(
          {
            kind: 'subtitles',
            label: sub.label,
            srclang: sub.lang,
            src: sub.src,
            default: sub.isDefault,
          },
          false
        )
      }
    })
  }
}

function togglePlay() {
  if (!player) return
  if (player.paused()) {
    player.play().catch(() => {})
  } else {
    player.pause()
  }
  resetHideTimer()
}

function toggleMute() {
  if (!player) return
  const newMuted = !player.muted()
  player.muted(newMuted)
  isMuted.value = newMuted
}

function onSeek(time: number) {
  if (!player) return
  player.currentTime(time)
  currentTime.value = time
  resetHideTimer()
}

function toggleFullscreen() {
  if (!videoContainerRef.value) return

  if (!document.fullscreenElement) {
    videoContainerRef.value.requestFullscreen().then(() => {
      isFullscreen.value = true
    }).catch(() => {})
  } else {
    document.exitFullscreen().then(() => {
      isFullscreen.value = false
    }).catch(() => {})
  }
}

function setSubtitle(lang: string) {
  activeSubtitle.value = lang
  showSubtitleMenu.value = false
  if (!player) return

  const tracks = player.textTracks?.()
  if (tracks) {
    for (let i = 0; i < tracks.length; i++) {
      if (lang === 'off') {
        tracks[i].mode = 'disabled'
      } else {
        const isMatch = tracks[i].language?.toLowerCase().startsWith(lang) ||
                        tracks[i].label?.toLowerCase().includes(lang === 'es' ? 'español' : 'english')
        tracks[i].mode = isMatch ? 'showing' : 'disabled'
      }
    }
  }
}

function setAudio(lang: string) {
  activeAudio.value = lang
  showAudioMenu.value = false
  if (!player) return

  const audioTracks = player.audioTracks?.()
  if (audioTracks) {
    for (let i = 0; i < audioTracks.length; i++) {
      const isSpanish = audioTracks[i].language?.toLowerCase().startsWith('es') ||
                        audioTracks[i].label?.toLowerCase().includes('español')
      audioTracks[i].enabled = (lang === 'es' ? isSpanish : !isSpanish)
    }
  }
}

function retryPlayback() {
  hasError.value = false
  errorMessage.value = ''
  if (player) {
    player.reset()
    player.src({
      src: props.episode.videoUrl,
      type: props.episode.videoUrl.endsWith('.m3u8') ? 'application/x-mpegURL' : 'video/mp4',
    })
    player.load()
    player.play().catch(() => {})
  }
}

watch(
  () => props.episode,
  newEp => {
    if (isExternalEmbed.value) {
      if (player) {
        player.dispose()
        player = null
      }
      return
    }

    if (player && newEp) {
      hasError.value = false
      player.src({
        src: newEp.videoUrl,
        type: newEp.videoUrl.endsWith('.m3u8') ? 'application/x-mpegURL' : 'video/mp4',
      })
      setupSubtitles(newEp.subtitles)
      player.load()
      currentTime.value = 0
      duration.value = newEp.duration || 0
      isPlaying.value = false
      showControls.value = true
    } else if (!player && !isExternalEmbed.value) {
      initPlayer()
    }
  }
)

onMounted(() => {
  initPlayer()

  document.addEventListener('fullscreenchange', () => {
    isFullscreen.value = !!document.fullscreenElement
  })
})

onBeforeUnmount(() => {
  if (hideControlsTimer) clearTimeout(hideControlsTimer)
  if (player) {
    player.dispose()
    player = null
  }
})
</script>

<template>
  <div
    ref="videoContainerRef"
    :class="[
      'relative w-full mx-auto bg-black overflow-hidden select-none group flex items-center justify-center transition-all',
      isFullscreen
        ? 'fixed inset-0 z-50 w-screen h-screen'
        : 'aspect-[9/16] max-w-sm sm:max-w-md rounded-2xl shadow-2xl border border-surface-border'
    ]"
    @mousemove="resetHideTimer"
    @touchstart="resetHideTimer"
  >
    <!-- ReelShort Embedded Player -->
    <div
      v-if="isReelShort"
      class="w-full h-full bg-black flex items-center justify-center relative"
    >
      <iframe
        :src="episode.videoUrl"
        class="w-full h-full border-0 rounded-2xl"
        allow="autoplay; fullscreen; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>

    <!-- Video.js Mobile Phone Vertical Stage (9:16 Microdramas with black bars on desktop) -->
    <div
      v-else
      :class="[
        'relative bg-black flex items-center justify-center overflow-hidden transition-all',
        isFullscreen
          ? 'h-full aspect-[9/16] max-w-[calc(100vh*9/16)] shadow-2xl border-x border-white/10'
          : 'w-full h-full'
      ]"
    >
      <video
        ref="videoElementRef"
        class="video-js vjs-default-skin w-full h-full object-contain"
        playsinline
        webkit-playsinline
      ></video>

      <!-- Tap Area for Play/Pause -->
      <div
        class="absolute inset-0 z-10 cursor-pointer"
        @click="togglePlay"
      ></div>

      <!-- Error State Overlay -->
      <div
        v-if="hasError"
        class="absolute inset-0 z-30 bg-black/90 flex flex-col items-center justify-center p-6 text-center gap-4"
      >
        <div class="w-14 h-14 rounded-full bg-primary/20 text-primary flex items-center justify-center">
          <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <div>
          <h4 class="text-base font-bold text-white mb-1">Error de Reproducción</h4>
          <p class="text-xs text-text-muted">{{ errorMessage }}</p>
        </div>
        <button
          @click.stop="retryPlayback"
          class="px-5 py-2 rounded-xl bg-primary hover:bg-primary-hover text-white text-xs font-semibold shadow-glow-primary transition-all"
        >
          Reintentar video
        </button>
      </div>

      <!-- Top Episode Info Overlay -->
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="-translate-y-full opacity-0"
        enter-to-class="translate-y-0 opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="translate-y-0 opacity-100"
        leave-to-class="-translate-y-full opacity-0"
      >
        <div
          v-if="showControls"
          class="absolute top-0 inset-x-0 z-20 p-4 bg-gradient-to-b from-black/90 via-black/40 to-transparent flex items-start justify-between pointer-events-auto"
        >
          <div>
            <span class="text-[11px] font-bold tracking-wider uppercase text-primary">
              Capítulo {{ episode.episodeNumber }}
            </span>
            <h3 class="text-sm font-bold text-white truncate max-w-[180px] sm:max-w-xs">
              {{ episode.title }}
            </h3>
            <p v-if="seriesTitle" class="text-[11px] text-text-muted truncate max-w-[180px]">
              {{ seriesTitle }}
            </p>
          </div>

          <!-- Top Action Badges: Audio & Subtitles -->
          <div class="flex items-center gap-1.5">
            <!-- Audio Selector Button -->
            <div class="relative">
              <button
                @click.stop="showAudioMenu = !showAudioMenu; showSubtitleMenu = false"
                :class="[
                  'px-2 py-1 rounded-lg text-[11px] font-bold border transition-colors flex items-center gap-1',
                  activeAudio === 'es'
                    ? 'bg-primary/20 text-primary border-primary/40'
                    : 'bg-black/50 text-white/80 border-white/10 hover:text-white'
                ]"
                title="Idioma del Audio"
              >
                <span>🔊</span>
                <span>{{ activeAudio === 'es' ? 'Audio ES' : 'Audio EN' }}</span>
              </button>

              <!-- Audio Dropdown -->
              <div
                v-if="showAudioMenu"
                class="absolute right-0 mt-2 w-32 glass-panel rounded-xl p-1.5 shadow-xl border border-surface-border z-30"
              >
                <button
                  @click.stop="setAudio('es')"
                  :class="[
                    'w-full text-left px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
                    activeAudio === 'es' ? 'bg-primary text-white' : 'text-text-muted hover:text-white'
                  ]"
                >
                  Español
                </button>
                <button
                  @click.stop="setAudio('en')"
                  :class="[
                    'w-full text-left px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
                    activeAudio === 'en' ? 'bg-primary text-white' : 'text-text-muted hover:text-white'
                  ]"
                >
                  Inglés (Original)
                </button>
              </div>
            </div>

            <!-- Subtitles Button -->
            <div class="relative">
              <button
                @click.stop="showSubtitleMenu = !showSubtitleMenu; showAudioMenu = false"
                :class="[
                  'px-2 py-1 rounded-lg text-[11px] font-bold border transition-colors flex items-center gap-1',
                  activeSubtitle !== 'off'
                    ? 'bg-secondary/20 text-secondary border-secondary/40'
                    : 'bg-black/50 text-white/80 border-white/10 hover:text-white'
                ]"
                title="Subtítulos / Subtitles"
              >
                <span>CC</span>
                <span>{{ activeSubtitle === 'es' ? 'ES' : (activeSubtitle === 'en' ? 'EN' : 'OFF') }}</span>
              </button>

              <!-- Subtitle Dropdown -->
              <div
                v-if="showSubtitleMenu"
                class="absolute right-0 mt-2 w-40 glass-panel rounded-xl p-1.5 shadow-xl border border-surface-border z-30"
              >
                <button
                  @click.stop="setSubtitle('es')"
                  :class="[
                    'w-full text-left px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
                    activeSubtitle === 'es' ? 'bg-primary text-white' : 'text-text-muted hover:text-white'
                  ]"
                >
                  Español (ES)
                </button>
                <button
                  @click.stop="setSubtitle('en')"
                  :class="[
                    'w-full text-left px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
                    activeSubtitle === 'en' ? 'bg-primary text-white' : 'text-text-muted hover:text-white'
                  ]"
                >
                  English (EN)
                </button>
                <button
                  @click.stop="setSubtitle('off')"
                  :class="[
                    'w-full text-left px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
                    activeSubtitle === 'off' ? 'bg-primary text-white' : 'text-text-muted hover:text-white'
                  ]"
                >
                  Desactivados / Off
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Center Big Play Button (when paused) -->
      <div
        v-if="!isPlaying && !hasError"
        class="absolute inset-0 z-20 flex items-center justify-center pointer-events-none"
      >
        <div class="w-16 h-16 rounded-full bg-primary/90 text-white flex items-center justify-center shadow-glow-primary transform scale-100 animate-pulse">
          <svg class="w-8 h-8 fill-current translate-x-1" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
        </div>
      </div>

      <!-- Bottom Controls Overlay -->
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="translate-y-full opacity-0"
        enter-to-class="translate-y-0 opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="translate-y-0 opacity-100"
        leave-to-class="translate-y-full opacity-0"
      >
        <div
          v-if="showControls"
          class="absolute bottom-0 inset-x-0 z-20 p-4 bg-gradient-to-t from-black/95 via-black/60 to-transparent pointer-events-auto space-y-3"
        >
          <!-- Progress Bar -->
          <ProgressBar
            :currentTime="currentTime"
            :duration="duration"
            @seek="onSeek"
          />

          <!-- Controls Row -->
          <div class="flex items-center justify-between text-white text-xs">
            <div class="flex items-center gap-3">
              <!-- Play / Pause -->
              <button
                @click.stop="togglePlay"
                class="p-1 text-white hover:text-primary transition-colors"
                :title="isPlaying ? 'Pausar' : 'Reproducir'"
              >
                <svg v-if="isPlaying" class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                  <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
                </svg>
                <svg v-else class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z" />
                </svg>
              </button>

              <!-- Mute / Unmute -->
              <button
                @click.stop="toggleMute"
                class="p-1 text-white hover:text-primary transition-colors"
                :title="isMuted ? 'Activar sonido' : 'Silenciar'"
              >
                <svg v-if="isMuted" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                </svg>
              </button>

              <!-- Time Display -->
              <span class="font-mono text-[11px] text-text-muted">
                {{ formattedCurrentTime }} / {{ formattedDuration }}
              </span>
            </div>

            <div class="flex items-center gap-2">
              <!-- Fullscreen -->
              <button
                @click.stop="toggleFullscreen"
                class="p-1 text-white hover:text-primary transition-colors"
                :title="isFullscreen ? 'Salir de pantalla completa' : 'Pantalla completa'"
              >
                <svg v-if="isFullscreen" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 9L4 4m0 0l5 0m-5 0l0 5M15 9l5-5m0 0l-5 0m5 0l0 5M9 15l-5 5m0 0l5 0m-5 0l0-5M15 15l5 5m0 0l-5 0m5 0l0-5" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0 0l-5-5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
/* Video.js custom container styling */
:deep(.video-js) {
  width: 100% !important;
  height: 100% !important;
  background-color: #000;
  font-family: inherit;
}

:deep(.vjs-tech) {
  object-fit: contain !important;
  width: 100% !important;
  height: 100% !important;
  margin: auto !important;
}

/* Yellow cinema subtitles with black outline and transparent background */
:deep(.vjs-text-track-display) {
  z-index: 15 !important;
  pointer-events: none !important;
  bottom: 75px !important;
}

:deep(.vjs-text-track-cue),
:deep(.vjs-text-track-cue div),
:deep(.vjs-text-track-display div) {
  background: transparent !important;
  background-color: transparent !important;
  color: #FFE600 !important; /* Bright Cinema Yellow */
  font-weight: 700 !important;
  font-size: 16px !important;
  line-height: 1.35 !important;
  letter-spacing: 0.02em !important;
  font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
  text-shadow: 
    -1.5px -1.5px 0 #000,  
     1.5px -1.5px 0 #000,
    -1.5px  1.5px 0 #000,
     1.5px  1.5px 0 #000,
     0px 2px 4px rgba(0,0,0,0.95),
     0px 0px 8px rgba(0,0,0,0.8) !important;
  padding: 0 !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}
</style>
