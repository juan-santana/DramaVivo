<script setup lang="ts">
import { useHead } from '@unhead/vue'

useHead({
  title: 'Política de Privacidad - DramaApp',
})
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-8">
    <div class="space-y-2 border-b border-surface-border pb-6">
      <span class="text-xs font-bold text-primary uppercase tracking-widest">Información Legal</span>
      <h1 class="text-3xl sm:text-4xl font-black text-white">Política de Privacidad</h1>
      <p class="text-xs text-text-muted">Última actualización: 16 de Octubre de 2026</p>
    </div>

    <div class="prose prose-invert prose-sm sm:prose-base max-w-none space-y-6 text-text-muted leading-relaxed">
      <section class="space-y-3">
        <h2 class="text-lg sm:text-xl font-bold text-white">1. Responsable del Tratamiento de Datos</h2>
        <p>
          En DramaApp nos tomamos muy en serio la privacidad y seguridad de nuestros usuarios. Esta política describe cómo tratamos la información personal recopilada a través de nuestra plataforma de streaming vertical.
        </p>
      </section>

      <section class="space-y-3">
        <h2 class="text-lg sm:text-xl font-bold text-white">2. Datos Recopilados y Almacenamiento Local</h2>
        <p>
          DramaApp opera con un enfoque prioritario en la privacidad del usuario:
        </p>
        <ul class="list-disc pl-5 space-y-1">
          <li><strong>Historial y Favoritos:</strong> Se almacenan de forma predeterminada localmente en tu propio navegador mediante Web Storage (localStorage).</li>
          <li><strong>Datos Técnicos de Reproducción:</strong> Registros anónimos de calidad de transmisión y buffering para optimizar la entrega de video HLS/MP4.</li>
          <li><strong>Datos de Cuenta (si aplica):</strong> Correo electrónico y credenciales cifradas para usuarios administradores o miembros registrados.</li>
        </ul>
      </section>

      <section class="space-y-3">
        <h2 class="text-lg sm:text-xl font-bold text-white">3. Finalidad del Tratamiento</h2>
        <p>
          Los datos se utilizan exclusivamente para garantizar la correcta reproducción en formato vertical 9:16, guardar tus preferencias de subtítulos y recordar los capítulos donde pausaste la visualización.
        </p>
      </section>

      <section class="space-y-3">
        <h2 class="text-lg sm:text-xl font-bold text-white">4. Ejercicio de Derechos (RGPD / GDPR)</h2>
        <p>
          Puedes solicitar el acceso, rectificación, supresión o portabilidad de cualquier dato enviando una comunicación al departamento legal a través del correo de soporte habilitado en la plataforma.
        </p>
      </section>
    </div>
  </div>
</template>
