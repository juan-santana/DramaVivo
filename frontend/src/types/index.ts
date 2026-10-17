// Core Domain Models for DramaApp

export interface Series {
  id: string
  title: string
  originalTitle?: string
  slug: string
  synopsis: string
  posterUrl: string
  bannerUrl?: string
  thumbnailUrl?: string
  verticalPosterUrl?: string
  releaseYear?: number
  genres: string[]
  language?: string
  subtitles?: string[]
  totalEpisodes?: number
  availableEpisodes?: number
  durationPerEpisode?: number // in seconds
  status?: 'ongoing' | 'completed' | 'announced' | string
  featured?: boolean
  trending?: boolean
  rating?: number
  viewsCount?: number
  views?: number
  likesCount?: number
  rightsStatus?: 'pending' | 'approved' | 'rejected' | 'under_review'
  sourceId?: string
  sourceName?: string
  sourceUrl?: string
  coverUrl?: string
  episodeCount?: number
  tags?: string[]
  createdAt?: string
  updatedAt?: string
}

export interface EpisodeSubtitle {
  lang: string
  label: string
  src?: string
  url?: string
  isDefault?: boolean
}

export interface Episode {
  id: string
  seriesId: string
  seriesTitle?: string
  episodeNumber: number
  seasonNumber?: number
  title: string
  synopsis?: string
  duration: number // in seconds
  thumbnailUrl?: string
  videoUrl: string
  subtitles?: EpisodeSubtitle[]
  isFree?: boolean
  quality?: string
  streamType?: string
  rightsStatus?: string
  viewsCount?: number
  likesCount?: number
  createdAt?: string
  updatedAt?: string
}

export interface Source {
  id: string
  name: string
  baseUrl: string
  scraperType: string
  enabled: boolean
  lastRunAt?: string
  lastRunStatus?: 'success' | 'failed' | 'running' | 'idle'
  totalDiscovered?: number
  totalImported?: number
  config?: Record<string, unknown>
  createdAt?: string
  updatedAt?: string
}

export interface RightsRecord {
  id: string
  seriesId: string
  seriesTitle: string
  holderName: string
  licenseType: 'exclusive' | 'non-exclusive' | 'public-domain' | 'pending-clearance'
  territory: string[]
  validFrom: string
  validUntil: string
  status: 'approved' | 'pending' | 'rejected' | 'under_review'
  notes?: string
  documentUrl?: string
  reviewedBy?: string
  reviewedAt?: string
  createdAt: string
  updatedAt?: string
}

export interface VideoAsset {
  id: string
  episodeId?: string
  seriesId?: string
  filename: string
  originalUrl?: string
  storagePath: string
  resolution: '720p' | '1080p' | '4k' | 'auto'
  aspectRatio: '9:16' | '16:9'
  format: 'mp4' | 'hls' | 'webm'
  fileSize: number // in bytes
  duration: number // in seconds
  status: 'uploading' | 'processing' | 'ready' | 'failed'
  transcodeProgress?: number
  createdAt: string
  updatedAt?: string
}

export interface ImportJob {
  id: string
  sourceId: string
  sourceName: string
  startedAt: string
  completedAt?: string
  status: 'running' | 'completed' | 'failed' | 'queued'
  recordsDiscovered: number
  recordsImported: number
  recordsSkipped: number
  recordsFailed: number
  errorMessage?: string
}

export interface DiscoveredSeries {
  id: string
  sourceId: string
  sourceName: string
  externalId: string
  title: string
  posterUrl: string
  synopsis: string
  episodeCount: number
  language: string
  discoveredAt: string
  status: 'pending' | 'imported' | 'blocked'
}

export interface TakedownRequest {
  id: string
  seriesId: string
  seriesTitle: string
  claimantName: string
  claimantEmail: string
  organization?: string
  reason: string
  status: 'pending' | 'resolved' | 'rejected'
  createdAt: string
  resolvedAt?: string
  notes?: string
}

export interface Genre {
  id: string
  name: string
  slug: string
  seriesCount?: number
  icon?: string
}

export interface SearchResult {
  query: string
  total: number
  series: Series[]
  genres?: Genre[]
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

export interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'editor' | 'viewer'
  avatarUrl?: string
  createdAt?: string
}

export interface AuthResponse {
  token: string
  user: User
}

export interface AnalyticsEvent {
  id: string
  eventType: 'view' | 'watch_time' | 'favorite' | 'search' | 'share' | 'ad_impression'
  seriesId?: string
  episodeId?: string
  userId?: string
  duration?: number
  device?: string
  country?: string
  timestamp: string
  metadata?: Record<string, unknown>
}

export interface AnalyticsSummary {
  totalViews: number
  watchTimeMinutes: number
  activeUsers: number
  topSeries: { seriesId: string; title: string; views: number; posterUrl?: string }[]
  trafficByDay: { date: string; views: number }[]
  totalSeries?: number
  totalEpisodes?: number
  completionRate?: number
  genreDistribution?: { genre: string; count: number; percentage: number }[]
  userHistoryCount?: number
  userFavoritesCount?: number
}

export interface WatchHistoryItem {
  seriesId: string
  episodeId: string
  episodeNumber: number
  seriesTitle: string
  posterUrl: string
  progressSeconds: number
  durationSeconds: number
  lastWatchedAt: string
}

export interface FavoriteItem {
  seriesId: string
  seriesTitle: string
  posterUrl: string
  genres: string[]
  totalEpisodes: number
  addedAt: string
}
