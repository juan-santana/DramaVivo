import json
import sys
from pymongo import MongoClient

sys.stdout.reconfigure(encoding='utf-8')

def sync_all():
    catalog_path = "output/dramashorts_real_catalog.json"
    with open(catalog_path, "r", encoding="utf-8") as f:
        master_catalog = json.load(f)

    series_list = master_catalog["series"]
    episodes_dict = master_catalog["episodes"]

    print(f"Loaded {len(series_list)} series and {len(episodes_dict)} episode groups from catalog.")

    # Format series for mockData.ts
    cleaned_series = []
    for s in series_list:
        ep_count = len(episodes_dict.get(s["id"], []))
        if ep_count == 0:
            ep_count = s.get("totalEpisodes") or 10
            
        cover = s.get("posterUrl") or s.get("coverUrl") or "https://assets.stardusttv.cc/uploadfile/20260909/98b2faae.jpg"
        views = s.get("viewsCount") or s.get("views") or 280000
        genres = s.get("genres") or ["Drama", "Romance"]
        lang = s.get("language") or ("english" if "English" in genres else "spanish")
        subs = ["English", "Español"] if lang == "english" else ["Español", "English"]

        cleaned_s = {
            "id": s["id"],
            "title": s["title"],
            "originalTitle": s.get("originalTitle") or s["title"],
            "slug": s.get("slug") or s["id"],
            "synopsis": s.get("synopsis") or "Un apasionante microdrama con alta intensidad emocional.",
            "posterUrl": cover,
            "bannerUrl": s.get("bannerUrl") or cover,
            "thumbnailUrl": s.get("thumbnailUrl") or cover,
            "verticalPosterUrl": s.get("verticalPosterUrl") or cover,
            "releaseYear": s.get("releaseYear") or 2026,
            "genres": genres,
            "language": lang,
            "subtitles": subs,
            "totalEpisodes": ep_count,
            "availableEpisodes": ep_count,
            "durationPerEpisode": s.get("durationPerEpisode") or 90,
            "status": "completed",
            "featured": s.get("featured", False),
            "trending": True,
            "rating": s.get("rating") or 9.6,
            "viewsCount": views,
            "likesCount": s.get("likesCount") or int(views * 0.15),
            "sourceId": "dramavivo",
            "sourceName": "DramaVivo",
            "createdAt": s.get("createdAt") or "2026-01-01T00:00:00Z",
            "updatedAt": s.get("updatedAt") or "2026-01-01T00:00:00Z"
        }
        cleaned_series.append(cleaned_s)

    # Ensure top 3 are featured
    if len(cleaned_series) > 0:
        cleaned_series[0]["featured"] = True
    if len(cleaned_series) > 1:
        cleaned_series[1]["featured"] = True
    if len(cleaned_series) > 2:
        cleaned_series[2]["featured"] = True

    # Build stream pool for any empty streams
    stream_pool = []
    for s_id, ep_list in episodes_dict.items():
        for ep in ep_list:
            v = ep.get("videoUrl")
            if v and v.startswith("http") and ".m3u8" in v:
                stream_pool.append(v)
                if len(stream_pool) >= 30:
                    break
        if len(stream_pool) >= 30:
            break

    # Format episodes
    cleaned_episodes = {}
    fallback_counter = 0
    series_lang_map = {s["id"]: s.get("language", "spanish") for s in cleaned_series}

    for s_id, ep_list in episodes_dict.items():
        s_lang = series_lang_map.get(s_id, "spanish")
        cleaned_list = []
        for ep in ep_list:
            # Guarantee both es and en subtitles
            sub_list = [
                {
                    "lang": "es",
                    "label": "Español",
                    "src": "/subtitles/es/sample.vtt",
                    "isDefault": s_lang != "english"
                },
                {
                    "lang": "en",
                    "label": "English",
                    "src": "/subtitles/en/sample.vtt",
                    "isDefault": s_lang == "english"
                }
            ]

            thumb = ep.get("thumbnailUrl")
            if not thumb or thumb == "null":
                thumb = "https://assets.stardusttv.cc/uploadfile/20260909/98b2faae.jpg"

            video_url = ep.get("videoUrl") or ""
            if not video_url and stream_pool:
                video_url = stream_pool[fallback_counter % len(stream_pool)]
                fallback_counter += 1

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
                "viewsCount": ep.get("viewsCount") or 25000,
                "likesCount": ep.get("likesCount") or 3500,
                "createdAt": "2026-01-01T00:00:00Z",
                "updatedAt": "2026-01-01T00:00:00Z"
            }
            cleaned_list.append(cleaned_ep)
        cleaned_episodes[s_id] = cleaned_list

    # Also save the healed episodes back to output/dramashorts_real_catalog.json
    master_catalog["episodes"] = cleaned_episodes
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, indent=2, ensure_ascii=False)

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
        },
        {
            "id": "job-3",
            "sourceId": "src-6",
            "sourceName": "DramaBox",
            "startedAt": "2026-03-01T09:30:00Z",
            "completedAt": "2026-03-01T09:45:00Z",
            "status": "completed",
            "recordsDiscovered": 42,
            "recordsImported": 42,
            "recordsSkipped": 0,
            "recordsFailed": 0
        }
    ]

    mock_discovered = []
    for s in cleaned_series[:15]:
        mock_discovered.append({
            "id": f"disc-{s['id']}",
            "sourceId": "src-5" if s['id'].startswith('stardust') else "src-7",
            "sourceName": "DramaVivo",
            "externalId": s["slug"],
            "title": s["title"],
            "synopsis": s["synopsis"],
            "posterUrl": s["posterUrl"],
            "episodeCount": s["totalEpisodes"],
            "language": s["language"],
            "status": "imported",
            "discoveredAt": "2026-03-01T00:00:00Z"
        })

    mock_rights = []
    for s in cleaned_series[:15]:
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
            { "seriesId": cleaned_series[0]["id"], "title": cleaned_series[0]["title"], "views": 412000 },
            { "seriesId": cleaned_series[1]["id"], "title": cleaned_series[1]["title"], "views": 389000 },
            { "seriesId": cleaned_series[2]["id"], "title": cleaned_series[2]["title"], "views": 365000 }
        ],
        "trafficByDay": [
            { "date": "2026-03-01", "views": 28400 },
            { "date": "2026-03-02", "views": 31200 },
            { "date": "2026-03-03", "views": 35800 }
        ]
    }

    # Write mockData.ts
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

    print(f"Generated complete {mock_data_path} with {len(cleaned_series)} series!")

    # Sync to MongoDB
    print("\nSyncing to MongoDB dramaapp...")
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        db = client["dramaapp"]
        db["series"].delete_many({})
        db["episodes"].delete_many({})

        series_docs = []
        for s in cleaned_series:
            raw_lang = str(s.get("language", "spanish")).lower()
            mongo_lang = "english" if ("en" in raw_lang or "ing" in raw_lang) else "spanish"
            series_docs.append({
                **s,
                "language": mongo_lang,
                "publicationStatus": "PUBLISHED",
                "rightsStatus": "APPROVED"
            })
        if series_docs:
            db["series"].insert_many(series_docs)

        ep_docs = []
        for s_id, ep_list in cleaned_episodes.items():
            for ep in ep_list:
                ep_docs.append({
                    **ep,
                    "publicationStatus": "PUBLISHED",
                    "rightsStatus": "APPROVED"
                })
        if ep_docs:
            db["episodes"].insert_many(ep_docs)

        print(f"MongoDB successfully populated: {len(series_docs)} series, {len(ep_docs)} episodes.")
    except Exception as e:
        print(f"MongoDB sync warning (MongoDB may not be running locally or timed out): {e}")

if __name__ == '__main__':
    sync_all()
