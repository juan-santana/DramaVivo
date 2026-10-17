import json
import shutil

cat_src = "output/dramashorts_real_catalog.json"
cat_dest = r"E:\DramaApp\frontend\src\services\catalog.json"

shutil.copyfile(cat_src, cat_dest)
print(f"Copied catalog JSON to {cat_dest}")

with open(cat_src, 'r', encoding='utf-8') as f:
    data = json.load(f)

series = data['series']
episodes = data['episodes']

# Ensure top 3 featured
if len(series) > 0: series[0]['featured'] = True
if len(series) > 1: series[1]['featured'] = True
if len(series) > 2: series[2]['featured'] = True

with open(cat_dest, 'w', encoding='utf-8') as f:
    json.dump({"series": series, "episodes": episodes}, f, indent=2, ensure_ascii=False)

mock_genres = [
    { "id": "1", "name": "Romance", "slug": "romance", "icon": "❤️" },
    { "id": "2", "name": "Venganza", "slug": "venganza", "icon": "⚔️" },
    { "id": "3", "name": "Multimillonario", "slug": "multimillonario", "icon": "💎" },
    { "id": "4", "name": "Fantasía", "slug": "fantasia", "icon": "✨" },
    { "id": "5", "name": "Pasión", "slug": "pasion", "icon": "🔥" },
    { "id": "6", "name": "Mafia", "slug": "mafia", "icon": "🕶️" },
    { "id": "7", "name": "Suspenso", "slug": "suspenso", "icon": "⚡" },
    { "id": "8", "name": "Dramas Cortos", "slug": "dramas-cortos", "icon": "🎬" },
]

mock_sources = [
    {
        "id": "src-1",
        "name": "DramaShorts",
        "baseUrl": "https://dramashorts.io",
        "scraperType": "nextjs",
        "enabled": True,
        "totalDiscovered": 15,
        "totalImported": 15,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-03-01T00:00:00Z"
    },
    {
        "id": "src-2",
        "name": "GoodShort",
        "baseUrl": "https://www.goodshort.com",
        "scraperType": "vue_ssr",
        "enabled": True,
        "totalDiscovered": 12,
        "totalImported": 12,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-03-01T00:00:00Z"
    },
    {
        "id": "src-3",
        "name": "NetShort",
        "baseUrl": "https://netshort.com",
        "scraperType": "nextjs_app_router",
        "enabled": True,
        "totalDiscovered": 12,
        "totalImported": 12,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-03-01T00:00:00Z"
    },
    {
        "id": "src-4",
        "name": "ReelShort",
        "baseUrl": "https://www.reelshort.com",
        "scraperType": "aes_decryptor",
        "enabled": True,
        "totalDiscovered": 6,
        "totalImported": 6,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-03-01T00:00:00Z"
    },
    {
        "id": "src-5",
        "name": "StardustTV",
        "baseUrl": "https://www.stardusttv.net/es",
        "scraperType": "nuxt3_devalue",
        "enabled": True,
        "totalDiscovered": 31,
        "totalImported": 31,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-03-01T00:00:00Z"
    },
    {
        "id": "src-6",
        "name": "DramaBox",
        "baseUrl": "https://www.dramabox.com/es",
        "scraperType": "nextjs_dramabox",
        "enabled": True,
        "totalDiscovered": 42,
        "totalImported": 42,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-03-01T00:00:00Z"
    },
    {
        "id": "src-7",
        "name": "ShortTV",
        "baseUrl": "https://www.shorttv.live",
        "scraperType": "nuxt3_shorttv",
        "enabled": True,
        "totalDiscovered": 45,
        "totalImported": 45,
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-03-01T00:00:00Z"
    }
]

mock_import_jobs = [
    {
        "id": "job-1",
        "sourceId": "src-5",
        "sourceName": "StardustTV",
        "startedAt": "2026-03-01T10:00:00Z",
        "completedAt": "2026-03-01T10:05:00Z",
        "status": "completed",
        "recordsDiscovered": 31,
        "recordsImported": 31,
        "recordsSkipped": 0,
        "recordsFailed": 0
    },
    {
        "id": "job-2",
        "sourceId": "src-7",
        "sourceName": "ShortTV",
        "startedAt": "2026-03-01T10:06:00Z",
        "completedAt": "2026-03-01T10:12:00Z",
        "status": "completed",
        "recordsDiscovered": 45,
        "recordsImported": 45,
        "recordsSkipped": 0,
        "recordsFailed": 0
    }
]

mock_discovered = []
for s in series[:15]:
    mock_discovered.append({
        "id": f"disc-{s['id']}",
        "sourceId": "src-5" if s['id'].startswith('stardust') else "src-7",
        "sourceName": "DramaVivo",
        "externalId": s["slug"],
        "title": s["title"],
        "synopsis": s["synopsis"],
        "posterUrl": s["posterUrl"],
        "episodeCount": s["totalEpisodes"],
        "language": s.get("language", "spanish"),
        "status": "imported",
        "discoveredAt": "2026-03-01T00:00:00Z"
    })

mock_rights = []
for s in series[:15]:
    mock_rights.append({
        "id": f"rr-{s['id']}",
        "seriesId": s["id"],
        "seriesTitle": s["title"],
        "holderName": "DramaVivo Media Group",
        "licenseType": "exclusive",
        "status": "approved",
        "territory": ["GLOBAL"],
        "validFrom": "2026-01-01T00:00:00Z",
        "validUntil": "2030-01-01T00:00:00Z",
        "reviewedAt": "2026-01-01T00:00:00Z",
        "reviewedBy": "admin",
        "createdAt": "2026-01-01T00:00:00Z",
        "notes": "Verified and active license"
    })

mock_videos = [
    {
        "id": "vid-1",
        "filename": "stream_master.m3u8",
        "storagePath": "/vod/prod/hls/",
        "resolution": "1080p",
        "aspectRatio": "9:16",
        "format": "hls",
        "fileSize": 45000000,
        "duration": 90,
        "status": "ready",
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-01T00:00:00Z"
    }
]

mock_takedowns = []

mock_analytics = {
    "totalViews": 8940000,
    "watchTimeMinutes": 745000,
    "activeUsers": 142000,
    "topSeries": [
        { "seriesId": series[0]["id"], "title": series[0]["title"], "views": 412000 },
        { "seriesId": series[1]["id"], "title": series[1]["title"], "views": 389000 },
        { "seriesId": series[2]["id"], "title": series[2]["title"], "views": 365000 }
    ],
    "trafficByDay": [
        { "date": "2026-03-01", "views": 28400 },
        { "date": "2026-03-02", "views": 31200 },
        { "date": "2026-03-03", "views": 35800 }
    ]
}

mockdata_code = f"""import type {{
  Series,
  Episode,
  Genre,
  Source,
  ImportJob,
  DiscoveredSeries,
  RightsRecord,
  VideoAsset,
  TakedownRequest,
  AnalyticsSummary,
}} from '../types'
import catalogData from './catalog.json'

export const MOCK_GENRES: Genre[] = {json.dumps(mock_genres, ensure_ascii=False, indent=2)};

export const MOCK_SERIES: Series[] = catalogData.series as unknown as Series[];

export const MOCK_EPISODES: Record<string, Episode[]> = catalogData.episodes as unknown as Record<string, Episode[]>;

export const MOCK_SOURCES: Source[] = {json.dumps(mock_sources, ensure_ascii=False, indent=2)};

export const MOCK_IMPORT_JOBS: ImportJob[] = {json.dumps(mock_import_jobs, ensure_ascii=False, indent=2)};

export const MOCK_DISCOVERED: DiscoveredSeries[] = {json.dumps(mock_discovered, ensure_ascii=False, indent=2)};

export const MOCK_RIGHTS: RightsRecord[] = {json.dumps(mock_rights, ensure_ascii=False, indent=2)};

export const MOCK_VIDEOS: VideoAsset[] = {json.dumps(mock_videos, ensure_ascii=False, indent=2)};

export const MOCK_TAKEDOWNS: TakedownRequest[] = {json.dumps(mock_takedowns, ensure_ascii=False, indent=2)};

export const MOCK_ANALYTICS: AnalyticsSummary = {json.dumps(mock_analytics, ensure_ascii=False, indent=2)};
"""

with open(r"E:\DramaApp\frontend\src\services\mockData.ts", 'w', encoding='utf-8') as f:
    f.write(mockdata_code)

print("Generated super-lightweight mockData.ts backed by catalog.json!")
