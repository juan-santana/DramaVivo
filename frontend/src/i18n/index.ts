import { computed } from 'vue'
import { useLocaleStore } from '../stores/locale'

export const translations = {
  es: {
    // Navigation
    'nav.home': 'Inicio',
    'nav.catalog': 'Catálogo',
    'nav.myList': 'Mi Lista',
    'nav.search': 'Buscar',
    'nav.admin': 'Admin',
    'nav.language': 'Idioma',

    // Hero
    'hero.badge': 'DRAMAS CORTOS 100% GRATIS • SIN REGISTRO',
    'hero.subtitle': 'Los mejores microdramas verticales en español e inglés. Romance, venganza, multimillonarios y fantasía con episodios completos sin cortes.',
    'hero.watchNow': 'Ver Ahora',
    'hero.exploreCatalog': 'Explorar Catálogo',
    'hero.trending': 'Tendencias del Momento',
    'hero.recentlyAdded': 'Recién Agregados',
    'hero.editorialPicks': 'Selección Editorial',
    'hero.episodesCount': 'episodios',

    // Home Redesign
    'home.continueWatching': 'Continuar Viendo',
    'home.resume': 'Reanudar',
    'home.ep': 'Ep.',
    'home.top10': 'Top 10 en DramaVivo Hoy',
    'home.trendingNow': 'Tendencias en DramaVivo',
    'home.exploreGenres': 'Explorar por Género',
    'home.viewAll': 'Ver todos',
    'home.exclusive': 'Dramas Exclusivos DramaVivo',
    'home.ceos': '👑 CEOs y Multimillonarios',
    'home.revenge': '⚔️ Venganzas y Traición',
    'home.romance': '🔥 Romance y Pasión Prohibida',
    'home.stardustShorts': '✨ Estrenos StardustTV & ShortTV',

    // Catalog
    'catalog.title': 'Catálogo Completo',
    'catalog.subtitle': 'Explora más de 90 dramas exclusivos y más de 1,400 episodios disponibles al instante en alta definición.',
    'catalog.searchPlaceholder': 'Buscar por título, género o sinopsis...',
    'catalog.filterAll': 'Todos',
    'catalog.sortBy': 'Ordenar por',
    'catalog.newest': 'Más Recientes',
    'catalog.popular': 'Más Populares',
    'catalog.rating': 'Mejor Calificados',
    'catalog.sourceFilter': 'Plataforma',
    'catalog.languageFilter': 'Idioma',
    'catalog.langAll': 'Todos los idiomas',
    'catalog.langEs': 'Español',
    'catalog.langEn': 'English',
    'catalog.seriesFound': 'dramas encontrados',
    'catalog.noResults': 'No se encontraron series que coincidan con tu búsqueda.',
    'catalog.clearFilters': 'Limpiar filtros',

    // Search
    'search.title': 'Búsqueda Global',
    'search.subtitle': 'Encuentra cualquier drama por título en español o inglés, sinopsis o género.',
    'search.inputPlaceholder': 'Escribe el nombre de un drama, temática (ej. millonario, mafia, venganza)...',
    'search.recentSearches': 'Búsquedas populares:',
    'search.resultsFor': 'Resultados para',
    'search.noDramas': 'No encontramos resultados para tu búsqueda.',
    'search.tryDifferent': 'Intenta buscar con otras palabras clave en inglés o español.',

    // Series Detail
    'series.startWatching': 'Empezar a ver Ep. 1',
    'series.continueWatching': 'Continuar viendo',
    'series.synopsis': 'Sinopsis',
    'series.details': 'Detalles de la Serie',
    'series.genres': 'Géneros',
    'series.language': 'Idioma original',
    'series.source': 'Fuente',
    'series.episodesList': 'Lista de Episodios',
    'series.episode': 'Capítulo',
    'series.free': '100% Gratis',
    'series.rating': 'Calificación',
    'series.views': 'Visualizaciones',

    // Player
    'player.back': 'Volver a la serie',
    'player.prev': 'Episodio Anterior',
    'player.next': 'Siguiente Episodio',
    'player.audio': 'Audio',
    'player.subtitles': 'Subtítulos',
    'player.subsOff': 'Desactivados',
    'player.freeBadge': 'Acceso Libre • Sin Monedas',
    'player.playing': 'Reproduciendo',
    'player.cinemaMode': 'Modo Cine',

    // Footer
    'footer.rights': 'Todos los derechos reservados. Plataforma de visualización de dramas y microdramas cortos.',
    'footer.disclaimer': 'Contenido de acceso libre para fines de entretenimiento y demostración.',
    'footer.home': 'Inicio',
    'footer.catalog': 'Catálogo',
    'footer.search': 'Buscar',
    'footer.terms': 'Términos',
    'footer.privacy': 'Privacidad',
    'footer.cookies': 'Cookies',
  },
  en: {
    // Navigation
    'nav.home': 'Home',
    'nav.catalog': 'Catalog',
    'nav.myList': 'My List',
    'nav.search': 'Search',
    'nav.admin': 'Admin',
    'nav.language': 'Language',

    // Hero
    'hero.badge': '100% FREE SHORT DRAMAS • NO SIGN UP REQUIRED',
    'hero.subtitle': 'The best vertical microdramas in English and Spanish. Romance, revenge, billionaires and fantasy with full uncut episodes.',
    'hero.watchNow': 'Watch Now',
    'hero.exploreCatalog': 'Explore Catalog',
    'hero.trending': 'Trending Now',
    'hero.recentlyAdded': 'Recently Added',
    'hero.editorialPicks': 'Editorial Picks',
    'hero.episodesCount': 'episodes',

    // Home Redesign
    'home.continueWatching': 'Continue Watching',
    'home.resume': 'Resume',
    'home.ep': 'Ep.',
    'home.top10': 'Top 10 on DramaVivo Today',
    'home.trendingNow': 'Trending on DramaVivo',
    'home.exploreGenres': 'Explore by Genre',
    'home.viewAll': 'View all',
    'home.exclusive': 'DramaVivo Exclusives',
    'home.ceos': '👑 CEOs & Billionaires',
    'home.revenge': '⚔️ Fierce Revenge',
    'home.romance': '🔥 Romance & Forbidden Passion',
    'home.stardustShorts': '✨ New StardustTV & ShortTV Releases',

    // Catalog
    'catalog.title': 'Full Catalog',
    'catalog.subtitle': 'Explore over 90 exclusive dramas and 1,400+ episodes ready to stream instantly in HD.',
    'catalog.searchPlaceholder': 'Search by title, genre, or synopsis...',
    'catalog.filterAll': 'All',
    'catalog.sortBy': 'Sort by',
    'catalog.newest': 'Newest',
    'catalog.popular': 'Most Popular',
    'catalog.rating': 'Top Rated',
    'catalog.sourceFilter': 'Platform',
    'catalog.languageFilter': 'Language',
    'catalog.langAll': 'All languages',
    'catalog.langEs': 'Spanish',
    'catalog.langEn': 'English',
    'catalog.seriesFound': 'dramas found',
    'catalog.noResults': 'No series found matching your criteria.',
    'catalog.clearFilters': 'Clear filters',

    // Search
    'search.title': 'Global Search',
    'search.subtitle': 'Find any drama by English or Spanish title, synopsis, or genre.',
    'search.inputPlaceholder': 'Type a drama name or theme (e.g., billionaire, mafia, revenge)...',
    'search.recentSearches': 'Trending searches:',
    'search.resultsFor': 'Results for',
    'search.noDramas': 'No dramas found matching your search.',
    'search.tryDifferent': 'Try searching with different English or Spanish keywords.',

    // Series Detail
    'series.startWatching': 'Start Watching Ep. 1',
    'series.continueWatching': 'Continue Watching',
    'series.synopsis': 'Synopsis',
    'series.details': 'Series Details',
    'series.genres': 'Genres',
    'series.language': 'Original Language',
    'series.source': 'Source',
    'series.episodesList': 'Episode List',
    'series.episode': 'Episode',
    'series.free': '100% Free',
    'series.rating': 'Rating',
    'series.views': 'Views',

    // Player
    'player.back': 'Back to series',
    'player.prev': 'Previous Episode',
    'player.next': 'Next Episode',
    'player.audio': 'Audio',
    'player.subtitles': 'Subtitles',
    'player.subsOff': 'Subtitles Off',
    'player.freeBadge': 'Free Access • No Coins Needed',
    'player.playing': 'Now Playing',
    'player.cinemaMode': 'Cinema Mode',

    // Footer
    'footer.rights': 'All rights reserved. Short drama streaming platform.',
    'footer.disclaimer': 'Free access content provided for entertainment and demonstration purposes.',
    'footer.home': 'Home',
    'footer.catalog': 'Catalog',
    'footer.search': 'Search',
    'footer.terms': 'Terms',
    'footer.privacy': 'Privacy',
    'footer.cookies': 'Cookies',
  }
}

export type TranslationKey = keyof typeof translations['es']

export function useI18n() {
  const localeStore = useLocaleStore()

  function t(key: TranslationKey, fallback?: string): string {
    const loc = localeStore.currentLocale
    const dict = translations[loc] || translations.es
    return (dict as Record<string, string>)[key] || fallback || key
  }

  const currentLang = computed(() => localeStore.currentLocale)

  return {
    t,
    currentLang,
    setLocale: localeStore.setLocale,
    toggleLocale: localeStore.toggleLocale
  }
}
