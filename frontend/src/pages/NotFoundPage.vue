<script setup lang="ts">
import { useHead } from '@unhead/vue'

useHead({
  title: '404 - Página No Encontrada | DramaApp',
})
</script>

<template>
  <div class="min-h-[75vh] flex flex-col items-center justify-center text-center px-4 py-16 relative overflow-hidden">
    <!-- Background Glow -->
    <div class="absolute w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none -top-12"></div>

    <div class="relative z-10 max-w-md space-y-6">
      <div class="inline-block px-4 py-1.5 rounded-full bg-primary/20 border border-primary/30 text-primary text-xs font-mono font-bold tracking-widest uppercase">
        Error 404
      </div>

      <h1 class="text-6xl sm:text-7xl font-black text-white tracking-tight">
        Escena Perdida
      </h1>

      <p class="text-sm text-text-muted leading-relaxed">
        El drama o capítulo que estás buscando no existe, ha cambiado de enlace o pertenece a una temporada aún inédita.
      </p>

      <div class="pt-4 flex flex-col sm:flex-row items-center justify-center gap-3">
        <router-link
          to="/"
          class="w-full sm:w-auto px-6 py-3 rounded-xl bg-primary hover:bg-primary-hover text-white text-xs font-bold shadow-glow-primary transition-all flex items-center justify-center gap-2"
        >
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
            <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
          </svg>
          <span>Volver al Inicio</span>
        </router-link>

        <router-link
          to="/catalogo"
          class="w-full sm:w-auto px-6 py-3 rounded-xl bg-surface hover:bg-surface-light border border-surface-border text-white text-xs font-bold transition-all"
        >
          Explorar Catálogo
        </router-link>
      </div>
    </div>
  </div>
</template>
