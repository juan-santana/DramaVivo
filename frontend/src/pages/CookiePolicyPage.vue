<script setup lang="ts">
import { useHead } from '@unhead/vue'

useHead({
  title: 'Política de Cookies - DramaApp',
})
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-8">
    <div class="space-y-2 border-b border-surface-border pb-6">
      <span class="text-xs font-bold text-secondary uppercase tracking-widest">Transparencia y Privacidad</span>
      <h1 class="text-3xl sm:text-4xl font-black text-white">Política de Cookies</h1>
      <p class="text-xs text-text-muted">Última revisión: Octubre 2026</p>
    </div>

    <div class="space-y-6 text-sm text-text-muted leading-relaxed">
      <section class="space-y-2">
        <h2 class="text-lg font-bold text-white">¿Qué son las cookies y tecnologías similares?</h2>
        <p>
          Las cookies y el almacenamiento local (HTML5 localStorage) son pequeños ficheros que se guardan en tu navegador para permitir que la aplicación recuerde tus preferencias de reproducción de episodios.
        </p>
      </section>

      <section class="space-y-3">
        <h2 class="text-lg font-bold text-white">Tipos de cookies que empleamos</h2>
        <div class="space-y-2">
          <div class="p-4 rounded-xl bg-surface border border-surface-border">
            <h3 class="text-sm font-bold text-white">Cookies Técnicas Esenciales</h3>
            <p class="text-xs text-text-muted mt-1">
              Necesarias para gestionar la sesión de usuario, seguridad y reproducción fluida de archivos de video.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-surface border border-surface-border">
            <h3 class="text-sm font-bold text-white">Almacenamiento Local de Preferencias</h3>
            <p class="text-xs text-text-muted mt-1">
              Guarda tus episodios favoritos, la posición del segundo donde pausaste el video y tus opciones de subtítulos activadas.
            </p>
          </div>
        </div>
      </section>

      <section class="space-y-2">
        <h2 class="text-lg font-bold text-white">Cómo configurar o revocar tus preferencias</h2>
        <p>
          Puedes borrar en cualquier instante el almacenamiento local y las cookies desde los ajustes de privacidad de tu navegador web o mediante el banner de consentimiento presentado en la página principal.
        </p>
      </section>
    </div>
  </div>
</template>
