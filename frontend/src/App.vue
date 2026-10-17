<script setup lang="ts">
import { useHead } from '@unhead/vue'

useHead({
  titleTemplate: '%s',
  htmlAttrs: {
    lang: 'es',
    class: 'dark',
  },
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0, maximum-scale=5.0' },
    { name: 'theme-color', content: '#0a0a0f' },
  ],
})
</script>

<template>
  <router-view />
</template>
