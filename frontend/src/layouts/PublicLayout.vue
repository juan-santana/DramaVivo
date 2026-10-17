<script setup lang="ts">
import AppHeader from '../components/common/AppHeader.vue'
import AppFooter from '../components/common/AppFooter.vue'
import ConsentBanner from '../components/common/ConsentBanner.vue'
import Toast from '../components/common/Toast.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-background text-text-main selection:bg-primary selection:text-white">
    <!-- Header -->
    <AppHeader />

    <!-- Main Page Content -->
    <main class="flex-1 w-full">
      <router-view v-slot="{ Component }">
        <component :is="Component" :key="$route.fullPath" />
      </router-view>
    </main>

    <!-- Footer -->
    <AppFooter />

    <!-- GDPR / Cookie Consent Banner -->
    <ConsentBanner />

    <!-- Toast Notifications Stack -->
    <Toast />
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
