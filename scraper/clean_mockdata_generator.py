import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

catalog_path = "output/dramashorts_real_catalog.json"
with open(catalog_path, "r", encoding="utf-8") as f:
    master_catalog = json.load(f)

# Clean Series
cleaned_series = []
for s in master_catalog["series"]:
    ep_count = s.get("episodeCount") or 10
    cover = s.get("posterUrl") or s.get("coverUrl") or "https://acf.goodshort.com/placeholder.jpg"
    views = s.get("views") or 250000
    genres = s.get("genres") or ["Drama", "Romance"]
    
    cleaned_s = {
        "id": s["id"],
        "title": s["title"],
        "originalTitle": s.get("originalTitle") or s["title"],
        "slug": s.get("slug") or s["id"],
        "synopsis": s.get("synopsis") or "Un apasionante microdrama con alta intensidad.",
        "posterUrl": cover,
        "bannerUrl": s.get("bannerUrl") or cover,
        "thumbnailUrl": s.get("thumbnailUrl") or cover,
        "verticalPosterUrl": s.get("verticalPosterUrl") or cover,
        "releaseYear": s.get("releaseYear") or 2025,
        "genres": genres,
        "language": s.get("language") or "spanish",
        "subtitles": ["Español", "English"],
        "totalEpisodes": ep_count,
        "availableEpisodes": ep_count,
        "durationPerEpisode": 100,
        "status": s.get("status") if s.get("status") in ["completed", "ongoing", "announced"] else "completed",
        "featured": s.get("featured", False),
        "trending": True,
        "rating": s.get("rating") or 9.6,
        "viewsCount": views,
        "likesCount": int(views * 0.15),
        "sourceId": s.get("sourceId") or "dramashorts",
        "sourceName": s.get("sourceId", "dramashorts").capitalize(),
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    }
    cleaned_series.append(cleaned_s)

# Ensure at least first 3 are featured
if len(cleaned_series) > 0:
    cleaned_series[0]["featured"] = True
if len(cleaned_series) > 1:
    cleaned_series[1]["featured"] = True
if len(cleaned_series) > 2:
    cleaned_series[2]["featured"] = True

# Clean Episodes
cleaned_episodes = {}
for s_id, ep_list in master_catalog["episodes"].items():
    cleaned_list = []
    for ep in ep_list:
        sub_list = []
        for sub in ep.get("subtitles") or []:
            sub_url = sub.get("url") or sub.get("src") or ""
            sub_list.append({
                "lang": sub.get("lang") or "es",
                "label": sub.get("label") or "Español",
                "src": sub_url,
                "isDefault": sub.get("lang") == "es"
            })
            
        thumb = ep.get("thumbnailUrl")
        if not thumb or thumb == "null":
            thumb = "https://acf.goodshort.com/placeholder.jpg"
            
        video_url = ep.get("videoUrl") or ""
        
        cleaned_ep = {
            "id": ep["id"],
            "seriesId": ep["seriesId"],
            "seriesTitle": ep.get("seriesTitle") or "",
            "episodeNumber": ep.get("episodeNumber") or 1,
            "seasonNumber": 1,
            "title": ep.get("title") or f"Episodio {ep.get('episodeNumber', 1)}",
            "synopsis": ep.get("synopsis") or "",
            "duration": ep.get("duration") or 90,
            "thumbnailUrl": thumb,
            "videoUrl": video_url,
            "subtitles": sub_list,
            "isFree": True,
            "viewsCount": 15000,
            "likesCount": 2400,
            "createdAt": "2025-01-01T00:00:00Z",
            "updatedAt": "2025-01-01T00:00:00Z"
        }
        cleaned_list.append(cleaned_ep)
    cleaned_episodes[s_id] = cleaned_list

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
        "totalDiscovered": 23,
        "totalImported": 23,
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    },
    {
        "id": "src-2",
        "name": "GoodShort",
        "baseUrl": "https://www.goodshort.com",
        "scraperType": "vue_ssr",
        "enabled": True,
        "totalDiscovered": 12,
        "totalImported": 12,
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    },
    {
        "id": "src-3",
        "name": "NetShort",
        "baseUrl": "https://netshort.com",
        "scraperType": "nextjs_app_router",
        "enabled": True,
        "totalDiscovered": 12,
        "totalImported": 12,
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    },
    {
        "id": "src-4",
        "name": "ReelShort",
        "baseUrl": "https://www.reelshort.com",
        "scraperType": "aes_decryptor",
        "enabled": True,
        "totalDiscovered": 6,
        "totalImported": 6,
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    },
    {
        "id": "src-5",
        "name": "Dailymotion Compilations",
        "baseUrl": "https://www.dailymotion.com",
        "scraperType": "geo_player",
        "enabled": True,
        "totalDiscovered": 3,
        "totalImported": 3,
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    },
    {
        "id": "src-6",
        "name": "DramaBox",
        "baseUrl": "https://www.dramabox.com/es",
        "scraperType": "nextjs_dramabox",
        "enabled": True,
        "totalDiscovered": 12,
        "totalImported": 12,
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    }
]

mock_import_jobs = [
    {
        "id": "job-1",
        "sourceId": "src-1",
        "sourceName": "DramaShorts",
        "startedAt": "2025-01-01T00:00:00Z",
        "completedAt": "2025-01-01T00:05:00Z",
        "status": "completed",
        "recordsDiscovered": 23,
        "recordsImported": 23,
        "recordsSkipped": 0,
        "recordsFailed": 0
    },
    {
        "id": "job-2",
        "sourceId": "src-2",
        "sourceName": "GoodShort",
        "startedAt": "2025-01-01T00:06:00Z",
        "completedAt": "2025-01-01T00:10:00Z",
        "status": "completed",
        "recordsDiscovered": 12,
        "recordsImported": 12,
        "recordsSkipped": 0,
        "recordsFailed": 0
    },
    {
        "id": "job-3",
        "sourceId": "src-3",
        "sourceName": "NetShort",
        "startedAt": "2025-01-01T00:11:00Z",
        "completedAt": "2025-01-01T00:15:00Z",
        "status": "completed",
        "recordsDiscovered": 12,
        "recordsImported": 12,
        "recordsSkipped": 0,
        "recordsFailed": 0
    }
]

mock_discovered = [
    {
        "id": "disc-1",
        "sourceId": "src-2",
        "sourceName": "GoodShort",
        "externalId": "31001113972",
        "title": "Blood and Bones of the Disowned Daughter",
        "posterUrl": "https://acf.goodshort.com/videobook/202509/cover-eYCOTZ5w9r.jpg",
        "synopsis": "Natalie was once the Parson family's cherished daughter...",
        "episodeCount": 11,
        "language": "english",
        "discoveredAt": "2025-01-01T00:00:00Z",
        "status": "imported"
    }
]

mock_rights = [
    {
        "id": "rights-1",
        "seriesId": "gs-31001113972",
        "seriesTitle": "Blood and Bones of the Disowned Daughter",
        "holderName": "GoodShort Media",
        "licenseType": "non-exclusive",
        "territory": ["ES", "US", "LATAM"],
        "validFrom": "2025-01-01T00:00:00Z",
        "validUntil": "2030-01-01T00:00:00Z",
        "status": "approved",
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    }
]

mock_videos = [
    {
        "id": "vid-1",
        "filename": "origin1_yv1abvaagv.m3u8",
        "storagePath": "/mts/books/972/31001113972/",
        "resolution": "1080p",
        "aspectRatio": "9:16",
        "format": "hls",
        "fileSize": 45000000,
        "duration": 241,
        "status": "ready",
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    }
]

mock_takedowns = []

mock_analytics = {
    "totalViews": 4500000,
    "watchTimeMinutes": 320000,
    "activeUsers": 84000,
    "topSeries": [
        { "seriesId": "ds-1", "title": "Mi prometido me vendió a dos bestias ardientes", "views": 250000 },
        { "seriesId": "gs-31001113972", "title": "Blood and Bones of the Disowned Daughter", "views": 312000 }
    ],
    "trafficByDay": [
        { "date": "2025-01-01", "views": 12000 },
        { "date": "2025-01-02", "views": 15400 }
    ]
}

ts_code = f"""import type {{
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

export const MOCK_GENRES: Genre[] = {json.dumps(mock_genres, ensure_ascii=False, indent=2)};

export const MOCK_SERIES: Series[] = {json.dumps(cleaned_series, ensure_ascii=False, indent=2)};

export const MOCK_EPISODES: Record<string, Episode[]> = {json.dumps(cleaned_episodes, ensure_ascii=False, indent=2)};

export const MOCK_SOURCES: Source[] = {json.dumps(mock_sources, ensure_ascii=False, indent=2)};

export const MOCK_IMPORT_JOBS: ImportJob[] = {json.dumps(mock_import_jobs, ensure_ascii=False, indent=2)};

export const MOCK_DISCOVERED: DiscoveredSeries[] = {json.dumps(mock_discovered, ensure_ascii=False, indent=2)};

export const MOCK_RIGHTS: RightsRecord[] = {json.dumps(mock_rights, ensure_ascii=False, indent=2)};

export const MOCK_VIDEOS: VideoAsset[] = {json.dumps(mock_videos, ensure_ascii=False, indent=2)};

export const MOCK_TAKEDOWNS: TakedownRequest[] = {json.dumps(mock_takedowns, ensure_ascii=False, indent=2)};

export const MOCK_ANALYTICS: AnalyticsSummary = {json.dumps(mock_analytics, ensure_ascii=False, indent=2)};
"""

mock_data_path = r"E:\DramaApp\frontend\src\services\mockData.ts"
with open(mock_data_path, "w", encoding="utf-8") as f:
    f.write(ts_code)

print("Generated complete mockData.ts with all admin exports!")
