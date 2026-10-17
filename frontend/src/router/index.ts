import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import PublicLayout from '../layouts/PublicLayout.vue'
import AdminLayout from '../layouts/AdminLayout.vue'

// Public Pages
import HomePage from '../pages/HomePage.vue'
import CatalogPage from '../pages/CatalogPage.vue'
import SeriesPage from '../pages/SeriesPage.vue'
import PlayerPage from '../pages/PlayerPage.vue'
import SearchPage from '../pages/SearchPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import MyListPage from '../pages/MyListPage.vue'
import NotFoundPage from '../pages/NotFoundPage.vue'
import PrivacyPage from '../pages/PrivacyPage.vue'
import TermsPage from '../pages/TermsPage.vue'
import CookiePolicyPage from '../pages/CookiePolicyPage.vue'

// Admin Pages
import AdminLogin from '../pages/admin/AdminLogin.vue'
import AdminDashboard from '../pages/admin/AdminDashboard.vue'
import AdminSources from '../pages/admin/AdminSources.vue'
import AdminImportJobs from '../pages/admin/AdminImportJobs.vue'
import AdminDiscoveredCatalog from '../pages/admin/AdminDiscoveredCatalog.vue'
import AdminRights from '../pages/admin/AdminRights.vue'
import AdminSeries from '../pages/admin/AdminSeries.vue'
import AdminEpisodes from '../pages/admin/AdminEpisodes.vue'
import AdminVideos from '../pages/admin/AdminVideos.vue'
import AdminTakedowns from '../pages/admin/AdminTakedowns.vue'
import AdminAnalytics from '../pages/admin/AdminAnalytics.vue'

const routes: RouteRecordRaw[] = [
  // Public Section
  {
    path: '/',
    component: PublicLayout,
    children: [
      {
        path: '',
        name: 'home',
        component: HomePage,
        meta: { title: 'Inicio - DramaApp' },
      },
      {
        path: 'catalogo',
        name: 'catalog',
        component: CatalogPage,
        meta: { title: 'Catálogo de Microdramas - DramaApp' },
      },
      {
        path: 'serie/:id',
        name: 'series-detail',
        component: SeriesPage,
        meta: { title: 'Ver Serie - DramaApp' },
      },
      {
        path: 'reproducir/:seriesId/:episodeId?',
        name: 'player',
        component: PlayerPage,
        meta: { title: 'Reproductor - DramaApp' },
      },
      {
        path: 'buscar',
        name: 'search',
        component: SearchPage,
        meta: { title: 'Buscar Microdramas - DramaApp' },
      },
      {
        path: 'perfil',
        name: 'profile',
        component: ProfilePage,
        meta: { title: 'Mi Perfil y Favoritos - DramaVivo' },
      },
      {
        path: 'mi-lista',
        name: 'my-list',
        component: MyListPage,
        meta: { title: 'Mi Lista - DramaVivo' },
      },
      {
        path: 'privacidad',
        name: 'privacy',
        component: PrivacyPage,
        meta: { title: 'Política de Privacidad - DramaApp' },
      },
      {
        path: 'terminos',
        name: 'terms',
        component: TermsPage,
        meta: { title: 'Términos de Servicio - DramaApp' },
      },
      {
        path: 'cookies',
        name: 'cookies',
        component: CookiePolicyPage,
        meta: { title: 'Política de Cookies - DramaApp' },
      },
      {
        path: ':pathMatch(.*)*',
        name: 'not-found',
        component: NotFoundPage,
        meta: { title: 'Página no encontrada - DramaApp' },
      },
    ],
  },

  // Admin Login (Standalone)
  {
    path: '/admin/login',
    name: 'admin-login',
    component: AdminLogin,
    meta: { title: 'Acceso Administrativo - DramaApp' },
  },

  // Admin Section (Protected)
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'admin-dashboard',
        component: AdminDashboard,
        meta: { title: 'Dashboard - Admin DramaApp' },
      },
      {
        path: 'fuentes',
        name: 'admin-sources',
        component: AdminSources,
        meta: { title: 'Fuentes Scraper - Admin DramaApp' },
      },
      {
        path: 'trabajos',
        name: 'admin-jobs',
        component: AdminImportJobs,
        meta: { title: 'Trabajos de Importación - Admin DramaApp' },
      },
      {
        path: 'descubiertos',
        name: 'admin-discovered',
        component: AdminDiscoveredCatalog,
        meta: { title: 'Catálogo Descubierto - Admin DramaApp' },
      },
      {
        path: 'derechos',
        name: 'admin-rights',
        component: AdminRights,
        meta: { title: 'Gestión de Derechos - Admin DramaApp' },
      },
      {
        path: 'series',
        name: 'admin-series',
        component: AdminSeries,
        meta: { title: 'Gestión de Series - Admin DramaApp' },
      },
      {
        path: 'episodios',
        name: 'admin-episodes',
        component: AdminEpisodes,
        meta: { title: 'Gestión de Episodios - Admin DramaApp' },
      },
      {
        path: 'videos',
        name: 'admin-videos',
        component: AdminVideos,
        meta: { title: 'Videos y Medios - Admin DramaApp' },
      },
      {
        path: 'reclamaciones',
        name: 'admin-takedowns',
        component: AdminTakedowns,
        meta: { title: 'Reclamaciones DMCA - Admin DramaApp' },
      },
      {
        path: 'analitica',
        name: 'admin-analytics',
        component: AdminAnalytics,
        meta: { title: 'Analítica y Audiencia - Admin DramaApp' },
      },
    ],
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  },
})

// Navigation Guard for Admin Routes
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('dramaapp_token')

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next({
        path: '/admin/login',
        query: { redirect: to.fullPath },
      })
      return
    }
  }

  // If visiting login while already authenticated, go to dashboard
  if (to.path === '/admin/login' && token) {
    next('/admin')
    return
  }

  next()
})
