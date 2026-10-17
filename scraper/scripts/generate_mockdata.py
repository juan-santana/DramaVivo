import json

with open('E:/DramaApp/scraper/output/dramashorts_real_catalog.json', 'r', encoding='utf-8') as f:
    saved = json.load(f)

series_list = saved['series']
episodes_dict = saved['episodes']

discovered_list = []
for i, s in enumerate(series_list):
    discovered_list.append({
        'id': f"disc-{i+1}",
        'sourceId': 'src-1',
        'sourceName': 'DramaShorts Oficial',
        'externalId': s['slug'],
        'title': s['title'],
        'posterUrl': s['posterUrl'],
        'synopsis': s['synopsis'],
        'episodeCount': s['totalEpisodes'],
        'language': 'es',
        'discoveredAt': '2026-10-16T19:48:00Z',
        'status': 'imported'
    })

mockdata_content = f"""import type {{ Series, Episode, Genre, Source, ImportJob, DiscoveredSeries, RightsRecord, VideoAsset, TakedownRequest, AnalyticsSummary }} from '../types'

export const MOCK_GENRES: Genre[] = [
  {{ id: '1', name: 'Romance', slug: 'romance', seriesCount: 18, icon: 'Heart' }},
  {{ id: '2', name: 'Venganza', slug: 'venganza', seriesCount: 14, icon: 'Flame' }},
  {{ id: '3', name: 'Drama', slug: 'drama', seriesCount: 22, icon: 'Film' }},
  {{ id: '4', name: 'Multimillonarios', slug: 'multimillonarios', seriesCount: 12, icon: 'Crown' }},
  {{ id: '5', name: 'Suspenso', slug: 'suspenso', seriesCount: 9, icon: 'Eye' }},
  {{ id: '6', name: 'Fantasía', slug: 'fantasia', seriesCount: 7, icon: 'Sparkles' }},
  {{ id: '7', name: 'Hombre Lobo', slug: 'hombre-lobo', seriesCount: 8, icon: 'Moon' }},
  {{ id: '8', name: 'LGBTQ+', slug: 'lgbtq', seriesCount: 6, icon: 'Rainbow' }},
]

export const MOCK_SERIES: Series[] = {json.dumps(series_list, indent=2, ensure_ascii=False)}

export const MOCK_EPISODES: Record<string, Episode[]> = {json.dumps(episodes_dict, indent=2, ensure_ascii=False)}

export const MOCK_SOURCES: Source[] = [
  {{
    id: 'src-1',
    name: 'DramaShorts Oficial',
    baseUrl: 'https://dramashorts.io/es',
    scraperType: 'dramashorts',
    enabled: true,
    lastRunAt: '2026-10-16T19:48:00Z',
    lastRunStatus: 'success',
    totalDiscovered: {len(series_list)},
    totalImported: {len(series_list)},
    config: {{ intervalHours: 6, respectRobotsTxt: true }},
    createdAt: '2026-01-01T00:00:00Z',
  }}
]

export const MOCK_IMPORT_JOBS: ImportJob[] = [
  {{
    id: 'job-101',
    sourceId: 'src-1',
    sourceName: 'DramaShorts Oficial',
    status: 'completed',
    startedAt: '2026-10-16T19:45:00Z',
    completedAt: '2026-10-16T19:48:00Z',
    recordsDiscovered: {len(series_list)},
    recordsImported: {len(series_list)},
    recordsSkipped: 0,
    recordsFailed: 0,
  }}
]

export const MOCK_DISCOVERED: DiscoveredSeries[] = {json.dumps(discovered_list, indent=2, ensure_ascii=False)}

export const MOCK_RIGHTS: RightsRecord[] = [
  {{
    id: 'rr-1',
    seriesId: 'ds-1',
    seriesTitle: 'El baile de medianoche del multimillonario',
    holderName: 'ShortDramas Global',
    licenseType: 'exclusive',
    territory: ['ES', 'MX', 'AR', 'CO', 'US'],
    validFrom: '2026-01-01T00:00:00Z',
    validUntil: '2028-12-31T23:59:59Z',
    status: 'approved',
    notes: 'Licencia para distribución gratuita con monetización publicitaria.',
    reviewedBy: 'Admin General',
    reviewedAt: '2026-01-05T10:00:00Z',
    createdAt: '2026-01-01T00:00:00Z',
  }}
]

export const MOCK_VIDEOS: VideoAsset[] = []
export const MOCK_TAKEDOWNS: TakedownRequest[] = []

export const MOCK_ANALYTICS: AnalyticsSummary = {{
  totalViews: {sum(s['viewsCount'] for s in series_list)},
  watchTimeMinutes: 142050,
  activeUsers: 8400,
  trafficByDay: [
    {{ date: '2026-10-10', views: 42100 }},
    {{ date: '2026-10-11', views: 48900 }},
    {{ date: '2026-10-12', views: 53200 }},
    {{ date: '2026-10-13', views: 61400 }},
    {{ date: '2026-10-14', views: 69800 }},
    {{ date: '2026-10-15', views: 78500 }},
    {{ date: '2026-10-16', views: 89400 }},
  ],
  topSeries: [
    {{ seriesId: 'ds-1', title: '{series_list[0]["title"] if series_list else "Drama"}', views: 125400 }},
    {{ seriesId: 'ds-2', title: '{series_list[1]["title"] if len(series_list) > 1 else "Drama 2"}', views: 98200 }},
  ],
}}
"""

with open('E:/DramaApp/frontend/src/services/mockData.ts', 'w', encoding='utf-8') as f:
    f.write(mockdata_content)

print("mockData.ts validado con TypeScript types!")
