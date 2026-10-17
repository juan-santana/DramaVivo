import { api } from './api'
import type { Series, Episode, Genre, PaginatedResponse, SearchResult } from '../types'
import { MOCK_SERIES, MOCK_EPISODES, MOCK_GENRES } from './mockData'

export const seriesService = {
  // Get all series with pagination, sorting and filtering
  async getAll(params?: {
    page?: number
    pageSize?: number
    genre?: string
    search?: string
    sort?: 'recent' | 'popular' | 'rating'
    language?: string
  }): Promise<PaginatedResponse<Series>> {
    let filtered = [...MOCK_SERIES]

    if (params?.genre && params.genre !== 'todos' && params.genre !== 'all') {
      const qg = params.genre.toLowerCase().trim()
      filtered = filtered.filter(s =>
        s.genres.some(g => {
          const gn = g.toLowerCase().trim()
          return gn === qg || gn.includes(qg) || qg.includes(gn)
        })
      )
    }

    if (params?.language && params.language !== 'todos' && params.language !== 'all') {
      const ql = params.language.toLowerCase().trim()
      filtered = filtered.filter(s => {
        const sl = (s.language || '').toLowerCase().trim()
        if (ql === 'es' || ql === 'español' || ql === 'spanish') return sl.includes('es') || sl.includes('span')
        if (ql === 'en' || ql === 'ingles' || ql === 'inglés' || ql === 'english') return sl.includes('en') || sl.includes('ing')
        return sl.includes(ql)
      })
    }

    if (params?.search) {
      const query = params.search.toLowerCase().trim()
      filtered = filtered.filter(s =>
        s.title.toLowerCase().includes(query) ||
        (s.originalTitle && s.originalTitle.toLowerCase().includes(query)) ||
        s.synopsis.toLowerCase().includes(query) ||
        s.genres.some(g => g.toLowerCase().includes(query))
      )
    }

    if (params?.sort === 'popular') {
      filtered.sort((a, b) => (b.viewsCount || 0) - (a.viewsCount || 0))
    } else if (params?.sort === 'rating') {
      filtered.sort((a, b) => (b.rating || 0) - (a.rating || 0))
    } else {
      filtered.sort((a, b) => new Date(b.createdAt || 0).getTime() - new Date(a.createdAt || 0).getTime())
    }

    const page = params?.page || 1
    const pageSize = params?.pageSize || 36
    const total = filtered.length
    const totalPages = Math.ceil(total / pageSize) || 1
    const start = (page - 1) * pageSize
    const data = filtered.slice(start, start + pageSize)

    return {
      data,
      total,
      page,
      pageSize,
      totalPages,
    }
  },

  // Get featured hero series
  async getFeatured(): Promise<Series[]> {
    const feat = MOCK_SERIES.filter(s => s.featured)
    return feat.length > 0 ? feat : [MOCK_SERIES[0]]
  },

  // Get trending series (return top viewed series so carousel is rich)
  async getTrending(): Promise<Series[]> {
    return [...MOCK_SERIES].sort((a, b) => (b.viewsCount || 0) - (a.viewsCount || 0)).slice(0, 8)
  },

  // Get recently added series (return all available series)
  async getRecent(limit = 30): Promise<Series[]> {
    return [...MOCK_SERIES].slice(0, limit)
  },

  // Get single series by ID, slug or title match
  async getById(idOrSlug: string): Promise<Series> {
    if (!idOrSlug) {
      return MOCK_SERIES[0]
    }

    const clean = idOrSlug.toLowerCase().trim()

    // 1. Direct match on id or slug
    const directMatch = MOCK_SERIES.find(
      s => s.id.toLowerCase() === clean || s.slug.toLowerCase() === clean
    )
    if (directMatch) return directMatch

    // 2. Partial match on slug or title
    const partialMatch = MOCK_SERIES.find(
      s =>
        s.slug.toLowerCase().includes(clean) ||
        clean.includes(s.slug.toLowerCase()) ||
        s.title.toLowerCase().includes(clean)
    )
    if (partialMatch) return partialMatch

    // 3. Fallback to API if available
    try {
      const res = await api.get<any>(`/series/${idOrSlug}`)
      if (res && res.title) {
        return {
          ...res,
          posterUrl: res.poster || res.posterUrl,
          bannerUrl: res.bannerUrl || res.poster || res.posterUrl,
          thumbnailUrl: res.poster || res.thumbnailUrl,
          verticalPosterUrl: res.verticalPosterUrl || res.poster || res.posterUrl,
        }
      }
    } catch {
      // Ignore API error
    }

    // 4. Safe fallback to first series so UI never shows blank error
    if (MOCK_SERIES.length > 0) {
      return MOCK_SERIES[0]
    }

    throw new Error('Serie no encontrada')
  },

  // Get episodes for a series (supports ID or slug)
  async getEpisodes(seriesIdOrSlug: string): Promise<Episode[]> {
    // Check if passed string is a slug or an ID
    const parent = MOCK_SERIES.find(
      s => s.id === seriesIdOrSlug || s.slug === seriesIdOrSlug
    )
    const targetId = parent ? parent.id : seriesIdOrSlug

    const episodes = MOCK_EPISODES[targetId]
    if (episodes && episodes.length > 0) {
      return episodes
    }

    // Check by any key
    for (const key of Object.keys(MOCK_EPISODES)) {
      if (key === targetId || (parent && key === parent.id)) {
        return MOCK_EPISODES[key]
      }
    }

    // Fallback to first available episodes list
    const firstKey = Object.keys(MOCK_EPISODES)[0]
    if (firstKey && MOCK_EPISODES[firstKey]) {
      return MOCK_EPISODES[firstKey]
    }

    return []
  },

  // Get single episode
  async getEpisodeById(seriesId: string, episodeId: string): Promise<Episode> {
    const list = await this.getEpisodes(seriesId)
    const ep = list.find(e => e.id === episodeId || String(e.episodeNumber) === String(episodeId))
    if (ep) return ep
    if (list.length > 0) return list[0]
    throw new Error('Episodio no encontrado')
  },

  // Get genres list with dynamically calculated accurate counts
  async getGenres(): Promise<Genre[]> {
    return MOCK_GENRES.map((genre: Genre) => {
      const qg = genre.name.toLowerCase().trim()
      const count = MOCK_SERIES.filter((s: Series) =>
        s.genres.some((g: string) => {
          const gn = g.toLowerCase().trim()
          return gn === qg || gn.includes(qg) || qg.includes(gn)
        })
      ).length
      return {
        ...genre,
        seriesCount: count,
      }
    }).filter((g: Genre) => (g.seriesCount || 0) > 0)
  },

  // Search series
  async search(query: string): Promise<SearchResult> {
    const q = query.toLowerCase().trim()
    const matches = MOCK_SERIES.filter((s: Series) =>
      s.title.toLowerCase().includes(q) ||
      (s.originalTitle && s.originalTitle.toLowerCase().includes(q)) ||
      s.synopsis.toLowerCase().includes(q) ||
      s.genres.some((g: string) => g.toLowerCase().includes(q))
    )
    const matchingGenres = MOCK_GENRES.filter((g: Genre) =>
      g.name.toLowerCase().includes(q)
    )

    return {
      query,
      total: matches.length,
      series: matches,
      genres: matchingGenres,
    }
  },
}
