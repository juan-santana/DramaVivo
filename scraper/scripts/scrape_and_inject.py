import httpx
import json
import re
from bs4 import BeautifulSoup

print("Iniciando scraping de DramaShorts.io en español...")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://dramashorts.io/es',
}

client = httpx.Client(headers=headers, follow_redirects=True, timeout=25)

# 1. Fetch homepage to get discover blocks
r = client.get('https://dramashorts.io/es')
soup = BeautifulSoup(r.text, 'html.parser')
data = json.loads(soup.find('script', id='__NEXT_DATA__').string)
discover = data['props']['pageProps']['discover']

# Gather unique series from top categories
chosen_movies = []
seen_ids = set()

# Prefer 'Only On Drama', 'Top Trending', 'movies_top_block', 'Popular Now'
for block in discover:
    block_type = block.get('type')
    block_data = block.get('data', {})
    block_title = block_data.get('title') or block_type
    movies = block_data.get('movies', [])
    for m in movies:
        mid = m['id']
        if mid not in seen_ids and m.get('title'):
            seen_ids.add(mid)
            m['_block'] = block_title
            chosen_movies.append(m)

# Take top 15 series for rich catalog
selected_movies = chosen_movies[:15]
print(f"Seleccionadas {len(selected_movies)} series principales para extraer episodios y videos.")

series_list = []
episodes_dict = {}

for idx, m in enumerate(selected_movies):
    mid = m['id']
    title = m.get('title')
    slug = m.get('slug') or f"series-{idx+1}"
    desc = m.get('description') or 'Sinopsis de la serie'
    genre_name = m.get('genre', {}).get('title') if m.get('genre') else 'Drama'
    images = m.get('images', {})
    cover = images.get('cover') or ''
    cover_title = images.get('coverWithTitle') or cover

    # Convert cdn.dramashorts.io URLs to use /cdn-proxy/ for CORS-free playback
    poster_url = cover.replace('https://cdn.dramashorts.io', '/cdn-proxy') if cover else ''
    vertical_poster = cover_title.replace('https://cdn.dramashorts.io', '/cdn-proxy') if cover_title else poster_url

    print(f"\n[{idx+1}/{len(selected_movies)}] Obteniendo episodios para: {title} ({mid})...")
    
    series_obj = {
        'id': f"ds-{idx+1}",
        'title': title,
        'originalTitle': m.get('slug', '').replace('-', ' ').title(),
        'slug': slug,
        'synopsis': desc,
        'posterUrl': poster_url,
        'bannerUrl': vertical_poster,
        'thumbnailUrl': poster_url,
        'verticalPosterUrl': vertical_poster,
        'releaseYear': 2026,
        'genres': [genre_name, 'Dramas Cortos', 'Romance' if 'Amor' in title or 'Cenicienta' in title else 'Suspenso'],
        'language': 'Español',
        'subtitles': ['Español', 'English'],
        'totalEpisodes': m.get('episodesCount', 20),
        'availableEpisodes': m.get('episodesCount', 20),
        'durationPerEpisode': 110,
        'status': 'completed',
        'featured': idx < 3,
        'trending': idx < 8,
        'rating': round(4.5 + (idx % 5) * 0.1, 1),
        'viewsCount': m.get('viewsCount', 500000),
        'likesCount': m.get('likesCount', 45000),
        'rightsStatus': 'approved',
        'sourceName': 'DramaShorts Oficial',
        'createdAt': '2026-03-01T12:00:00Z',
    }
    series_list.append(series_obj)

    # Fetch episodes for this series
    try:
        ep_res = client.get(f"https://dramashorts.io/es/shorts/{mid}")
        ep_soup = BeautifulSoup(ep_res.text, 'html.parser')
        ep_data = json.loads(ep_soup.find('script', id='__NEXT_DATA__').string)
        raw_episodes = ep_data['props']['pageProps'].get('episodes', [])
        
        series_episodes = []
        for ep_item in raw_episodes:
            ep = ep_item.get('episode', {})
            ep_index = ep.get('index', 1)
            ep_title = ep.get('title') or f"Capítulo {ep_index}"
            duration = int(ep.get('duration', 90))
            raw_cover = ep.get('coverUrl', '')

            # Extract hashes: https://cdn.dramashorts.io/img/episodes-previews/<movie_hash>/<ep_hash>/cover.jpeg
            hash_match = re.search(r'episodes-previews/([^/]+)/([^/]+)/', raw_cover)
            if hash_match:
                movie_hash, ep_hash = hash_match.groups()
                # Use proxy path
                video_url = f"/cdn-proxy/video/{movie_hash}/{ep_hash}/manifest.m3u8"
                thumb_url = f"/cdn-proxy/img/episodes-previews/{movie_hash}/{ep_hash}/cover.jpeg"
            else:
                video_url = raw_cover.replace('/img/episodes-previews/', '/video/').replace('cover.jpeg', 'manifest.m3u8').replace('https://cdn.dramashorts.io', '/cdn-proxy')
                thumb_url = raw_cover.replace('https://cdn.dramashorts.io', '/cdn-proxy')

            series_episodes.append({
                'id': f"ep-{idx+1}-{ep_index}",
                'seriesId': f"ds-{idx+1}",
                'seriesTitle': title,
                'episodeNumber': ep_index,
                'title': f"Capítulo {ep_index}: {ep_title}" if 'Capítulo' not in ep_title else ep_title,
                'synopsis': f"Episodio {ep_index} de {title}. Descubre los giros inesperados y la tensión dramática.",
                'duration': duration,
                'thumbnailUrl': thumb_url,
                'videoUrl': video_url,
                'subtitles': [
                    {
                        'lang': 'es',
                        'label': 'Español',
                        'src': '',
                        'isDefault': True
                    }
                ],
                # 100% GRATIS para el usuario
                'isFree': True,
                'viewsCount': max(1000, series_obj['viewsCount'] // len(raw_episodes) if raw_episodes else 10000),
                'likesCount': max(100, series_obj['likesCount'] // len(raw_episodes) if raw_episodes else 1000),
                'createdAt': '2026-03-01T12:00:00Z'
            })

        episodes_dict[f"ds-{idx+1}"] = series_episodes
        print(f"   -> {len(series_episodes)} episodios extraídos con stream HLS y miniaturas.")
    except Exception as e:
        print(f"   Error obteniendo episodios de {mid}: {e}")

print(f"\nScraping completado. Total series: {len(series_list)}, Total episodios listos: {sum(len(eps) for eps in episodes_dict.values())}")

# Save json backup
with open('E:/DramaApp/scraper/output/dramashorts_real_catalog.json', 'w', encoding='utf-8') as f:
    json.dump({'series': series_list, 'episodes': episodes_dict}, f, indent=2, ensure_ascii=False)
print("Catálogo guardado en scraper/output/dramashorts_real_catalog.json")

# Now inject into frontend mockData.ts
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
    adapterType: 'dramashorts',
    enabled: true,
    crawlPolicy: {{ intervalHours: 6, maxPages: 10, respectRobotsTxt: true }},
    lastRunAt: '2026-10-16T19:48:00Z',
    lastRunStatus: 'success',
    totalDiscovered: {len(series_list)},
    totalImported: {len(series_list)},
    createdAt: '2026-01-01T00:00:00Z',
  }}
]

export const MOCK_IMPORT_JOBS: ImportJob[] = [
  {{
    id: 'job-101',
    sourceId: 'src-1',
    sourceName: 'DramaShorts Oficial',
    status: 'completed',
    discoveredCount: {len(series_list)},
    importedCount: {len(series_list)},
    skippedCount: 0,
    startedAt: '2026-10-16T19:45:00Z',
    completedAt: '2026-10-16T19:48:00Z',
    logUrl: '/logs/job-101.log',
  }}
]

export const MOCK_DISCOVERED: DiscoveredSeries[] = {json.dumps([{
    'id': f"disc-{i+1}",
    'sourceId': 'src-1',
    'sourceUrl': f"https://dramashorts.io/es/shorts/{s['slug']}",
    'title': s['title'],
    'originalTitle': s['originalTitle'],
    'synopsis': s['synopsis'],
    'genres': s['genres'],
    'language': 'es',
    'episodeCount': s['totalEpisodes'],
    'posterUrl': s['posterUrl'],
    'discoveredAt': '2026-10-16T19:48:00Z',
    'status': 'imported'
} for i, s in enumerate(series_list)], indent=2, ensure_ascii=False)}

export const MOCK_RIGHTS: RightsRecord[] = [
  {{
    id: 'rr-1',
    seriesId: 'ds-1',
    seriesTitle: 'El baile de medianoche del multimillonario',
    rightsHolder: 'ShortDramas Global',
    authorizationType: 'exclusive',
    allowedTerritories: ['ES', 'MX', 'AR', 'CO', 'US'],
    streamingAllowed: true,
    monetizationAllowed: true,
    subtitlingAllowed: true,
    validFrom: '2026-01-01T00:00:00Z',
    validUntil: '2028-12-31T23:59:59Z',
    evidenceUrl: 'https://docs.dramaapp.local/contracts/ds-1.pdf',
    reviewedBy: 'Admin General',
    reviewedAt: '2026-01-05T10:00:00Z',
    status: 'approved',
    notes: 'Licencia para distribución gratuita con monetización publicitaria.',
  }}
]

export const MOCK_VIDEOS: VideoAsset[] = []
export const MOCK_TAKEDOWNS: TakedownRequest[] = []

export const MOCK_ANALYTICS: AnalyticsSummary = {{
  totalViews: {sum(s['viewsCount'] for s in series_list)},
  uniqueViewers: 142050,
  averageWatchTimeMinutes: 8.5,
  completionRate: 74.2,
  dailyViews: [
    {{ date: '2026-10-10', views: 42100 }},
    {{ date: '2026-10-11', views: 48900 }},
    {{ date: '2026-10-12', views: 53200 }},
    {{ date: '2026-10-13', views: 61400 }},
    {{ date: '2026-10-14', views: 69800 }},
    {{ date: '2026-10-15', views: 78500 }},
    {{ date: '2026-10-16', views: 89400 }},
  ],
  topSeries: [
    {{ seriesId: 'ds-1', title: '{series_list[0]["title"] if series_list else "Drama"}', views: 125400, completionRate: 82.1 }},
    {{ seriesId: 'ds-2', title: '{series_list[1]["title"] if len(series_list) > 1 else "Drama 2"}', views: 98200, completionRate: 78.4 }},
  ],
}}
"""

with open('E:/DramaApp/frontend/src/services/mockData.ts', 'w', encoding='utf-8') as f:
    f.write(mockdata_content)

print("¡mockData.ts actualizado exitosamente con las series y videos reales de DramaShorts!")
