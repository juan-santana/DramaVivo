<script setup lang="ts">
import { useI18n } from '../../i18n'

const { t, currentLang } = useI18n()
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="w-full bg-[#07070b] border-t border-surface-border text-text-muted mt-20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8 lg:gap-12">
        <!-- Brand column -->
        <div class="space-y-4 md:col-span-1">
          <router-link to="/" class="flex items-center gap-3">
            <div class="relative w-8 h-8 rounded-xl bg-[#12121a] border border-white/20 p-1.5 flex items-center justify-center shadow-lg">
              <svg class="w-full h-full" viewBox="0 0 32 32" fill="none">
                <path d="M6 7L16 25L26 7" stroke="url(#dv-f-gradient-1)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M11 7L16 16L21 7" stroke="url(#dv-f-gradient-2)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
                <circle cx="16" cy="16" r="2.2" fill="#F5C518" />
                <defs>
                  <linearGradient id="dv-f-gradient-1" x1="6" y1="7" x2="26" y2="25" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#FF2E55" />
                    <stop offset="0.5" stop-color="#FF9E00" />
                    <stop offset="1" stop-color="#9333EA" />
                  </linearGradient>
                  <linearGradient id="dv-f-gradient-2" x1="11" y1="7" x2="21" y2="16" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#FFD700" />
                    <stop offset="1" stop-color="#FF2E55" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <span class="text-xl font-black tracking-tight text-white">
              Drama<span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-rose-500 to-purple-400">Vivo</span>
            </span>
          </router-link>
          <p class="text-xs text-text-muted leading-relaxed">
            {{ currentLang === 'en'
              ? 'The leading vertical microdrama streaming platform in English and Spanish. Exciting romance, revenge, and fantasy in 2-minute episodes.'
              : 'La plataforma líder de microdramas y series verticales en español e inglés. Historias apasionantes, romances intensos y venganzas en episodios de 2 minutos diseñados para tu pantalla móvil.'
            }}
          </p>
        </div>

        <!-- Navigation -->
        <div>
          <h4 class="text-sm font-semibold text-white tracking-wider uppercase mb-4">
            {{ currentLang === 'en' ? 'Explore' : 'Explorar' }}
          </h4>
          <ul class="space-y-2.5 text-xs">
            <li>
              <router-link to="/" class="hover:text-white transition-colors">{{ t('nav.home') }}</router-link>
            </li>
            <li>
              <router-link to="/catalogo" class="hover:text-white transition-colors">{{ t('nav.catalog') }}</router-link>
            </li>
            <li>
              <router-link to="/buscar" class="hover:text-white transition-colors">{{ t('nav.search') }}</router-link>
            </li>
          </ul>
        </div>

        <!-- Genres -->
        <div>
          <h4 class="text-sm font-semibold text-white tracking-wider uppercase mb-4">
            Géneros Populares
          </h4>
          <ul class="space-y-2.5 text-xs">
            <li>
              <router-link to="/catalogo?genre=Romance" class="hover:text-white transition-colors">Romance y Pasión</router-link>
            </li>
            <li>
              <router-link to="/catalogo?genre=Venganza" class="hover:text-white transition-colors">Venganza y Traición</router-link>
            </li>
            <li>
              <router-link to="/catalogo?genre=Multimillonarios" class="hover:text-white transition-colors">CEOs y Multimillonarios</router-link>
            </li>
            <li>
              <router-link to="/catalogo?genre=Suspenso" class="hover:text-white transition-colors">Suspenso e Intriga</router-link>
            </li>
          </ul>
        </div>

        <!-- Legal -->
        <div>
          <h4 class="text-sm font-semibold text-white tracking-wider uppercase mb-4">
            Legal y Derechos
          </h4>
          <ul class="space-y-2.5 text-xs">
            <li>
              <router-link to="/terminos" class="hover:text-white transition-colors">Términos de Servicio</router-link>
            </li>
            <li>
              <router-link to="/privacidad" class="hover:text-white transition-colors">Política de Privacidad</router-link>
            </li>
            <li>
              <router-link to="/cookies" class="hover:text-white transition-colors">Política de Cookies</router-link>
            </li>
            <li>
              <router-link to="/admin/login" class="text-secondary/80 hover:text-secondary transition-colors">Portal Administrativo</router-link>
            </li>
          </ul>
        </div>
      </div>

      <!-- Copyright -->
      <div class="mt-12 pt-8 border-t border-surface-border flex flex-col sm:flex-row items-center justify-between text-xs text-text-muted gap-4">
        <p>© {{ currentYear }} DramaApp. Todos los derechos reservados. Formato de entretenimiento vertical en español.</p>
        <p class="text-[11px] text-text-dim">Optimizado para streaming vertical de alta fidelidad 9:16.</p>
      </div>
    </div>
  </footer>
</template>
