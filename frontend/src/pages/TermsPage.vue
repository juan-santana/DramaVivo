<script setup lang="ts">
import { useHead } from '@unhead/vue'

useHead({
  title: 'Términos de Servicio - DramaApp',
})
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-8">
    <div class="space-y-2 border-b border-surface-border pb-6">
      <span class="text-xs font-bold text-primary uppercase tracking-widest">Condiciones Generales</span>
      <h1 class="text-3xl sm:text-4xl font-black text-white">Términos de Servicio</h1>
      <p class="text-xs text-text-muted">En vigor desde: 16 de Octubre de 2026</p>
    </div>

    <div class="space-y-6 text-sm text-text-muted leading-relaxed">
      <section class="space-y-2">
        <h2 class="text-lg font-bold text-white">1. Aceptación de los Términos</h2>
        <p>
          Al acceder o interactuar con el sitio web y servicios de DramaApp, aceptas someterte a estos Términos de Servicio y a todas las directrices legales aplicables al consumo de contenidos audiovisuales.
        </p>
      </section>

      <section class="space-y-2">
        <h2 class="text-lg font-bold text-white">2. Propiedad Intelectual y Derechos Audiovisuales</h2>
        <p>
          Todos los microdramas, pistas de subtítulos, composiciones sonoras y marcas visuales mostradas en DramaApp son propiedad exclusiva de sus respectivos creadores y titulares de licencia. El usuario solo cuenta con una licencia personal, no transferible y no comercial para visualizarlos mediante el reproductor oficial.
        </p>
      </section>

      <section class="space-y-2">
        <h2 class="text-lg font-bold text-white">3. Procedimiento de Retirada y Notificaciones DMCA</h2>
        <p>
          DramaApp respeta estrictamente los derechos de autor. Cualquier titular que considere que un contenido vulnera sus derechos exclusivos puede notificarlo a nuestro equipo de moderación para su inmediata revisión y retirada cautelar.
        </p>
      </section>

      <section class="space-y-2">
        <h2 class="text-lg font-bold text-white">4. Uso Aceptable del Servicio</h2>
        <p>
          Queda expresamente prohibido extraer, descargar masivamente, descompilar o retransmitir los flujos de video sin consentimiento previo y por escrito de la plataforma.
        </p>
      </section>
    </div>
  </div>
</template>
