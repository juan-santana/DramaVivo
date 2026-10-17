import json
from datetime import datetime, timezone
from pymongo import MongoClient

cat_path = r"E:\DramaApp\scraper\output\dramashorts_real_catalog.json"
catalog = json.load(open(cat_path, encoding="utf-8"))

# Deduplicate series by slug and id
seen_slugs = set()
seen_ids = set()
unique_series = []
unique_episodes = {}

for s in catalog["series"]:
    slug = s["slug"].lower().strip()
    sid = s["id"]
    if slug in seen_slugs or sid in seen_ids:
        continue
    seen_slugs.add(slug)
    seen_ids.add(sid)
    unique_series.append(s)
    if sid in catalog["episodes"]:
        unique_episodes[sid] = catalog["episodes"][sid]

catalog["series"] = unique_series
catalog["episodes"] = unique_episodes

# Save back deduplicated catalog
with open(cat_path, "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print(f"Catalog deduplicated! Total unique series: {len(unique_series)}")

# 1. Update mockData.ts
mock_path = r"E:\DramaApp\frontend\src\services\mockData.ts"
with open(mock_path, "r", encoding="utf-8") as f:
    orig = f.read()

sources_idx = orig.find("export const MOCK_SOURCES")
sources_tail = orig[sources_idx:]
genres_end = orig.find("export const MOCK_SERIES: Series[] = [")
header = orig[:genres_end]

series_json = json.dumps(unique_series, ensure_ascii=False, indent=2)
episodes_json = json.dumps(unique_episodes, ensure_ascii=False, indent=2)

new_mock_content = f"""{header}export const MOCK_SERIES: Series[] = {series_json}

export const MOCK_EPISODES: Record<string, Episode[]> = {episodes_json}

{sources_tail}"""

with open(mock_path, "w", encoding="utf-8") as f:
    f.write(new_mock_content)

print(f"mockData.ts updated with {len(unique_series)} series!")

# 2. Sync to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dramaapp"]

now = datetime.now(timezone.utc)
series_docs = []
episode_docs = []

for s in unique_series:
    sid = s["id"]
    series_docs.append({
        "_id": sid,
        "slug": s["slug"],
        "title": s["title"],
        "originalTitle": s.get("originalTitle") or s["title"],
        "synopsis": s["synopsis"],
        "genres": s["genres"],
        "language": "spanish",
        "poster": s["posterUrl"],
        "sourceId": "src-1",
        "sourceUrl": s.get("sourceUrl") or f"https://dramashorts.io/es/shorts/{s['slug']}",
        "publicationStatus": "PUBLISHED",
        "rightsStatus": "APPROVED",
        "seoTitle": f"{s['title']} | Ver Episodios Gratis Online",
        "seoDescription": s["synopsis"][:150],
        "viewCount": s.get("viewsCount", 10000),
        "createdAt": now,
        "updatedAt": now,
        "_class": "com.dramaapp.model.Series"
    })
    
    for ep in unique_episodes.get(sid, []):
        episode_docs.append({
            "_id": ep["id"],
            "seriesId": sid,
            "seasonNumber": 1,
            "episodeNumber": ep["episodeNumber"],
            "title": ep["title"],
            "synopsis": ep["synopsis"],
            "durationSeconds": ep["duration"],
            "videoAssetId": ep["videoUrl"],
            "subtitleTracks": [
                {"language": "es", "label": "Español", "fileUrl": "", "isDefault": True}
            ],
            "thumbnail": ep["thumbnailUrl"],
            "publicationStatus": "PUBLISHED",
            "rightsStatus": "APPROVED",
            "createdAt": now,
            "updatedAt": now,
            "_class": "com.dramaapp.model.Episode"
        })

db.series.delete_many({})
db.episodes.delete_many({})
if series_docs:
    db.series.insert_many(series_docs)
if episode_docs:
    db.episodes.insert_many(episode_docs)

print(f"MongoDB successfully synced! Series: {db.series.count_documents({})}, Episodes: {db.episodes.count_documents({})}")
