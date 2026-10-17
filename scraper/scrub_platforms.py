import json
from pymongo import MongoClient

print("=== SCRUBBING PLATFORM NAMES FROM GENRES AND SOURCES ===")

cat_path = r"E:\DramaApp\scraper\output\dramashorts_real_catalog.json"
cat = json.load(open(cat_path, encoding='utf-8'))

forbidden = {"reelshort", "goodshort", "netshort", "dramabox", "dramashorts", "dailymotion", "shortmax", "src-1", "src-2", "src-3"}

for s in cat['series']:
    # Clean genres
    clean_genres = []
    for g in s.get('genres', []):
        if g.lower().strip() not in forbidden:
            clean_genres.append(g)
    if not clean_genres:
        clean_genres = ["Dramas Cortos", "Romance"]
    s['genres'] = clean_genres
    
    # Rebrand source
    s['sourceId'] = 'dramavivo'
    s['sourceName'] = 'DramaVivo Original' if s.get('featured') else 'DramaVivo Exclusivo'

# Save back to json
with open(cat_path, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=2)

# Update mockData.ts
mock_path = r"E:\DramaApp\frontend\src\services\mockData.ts"
with open(mock_path, "r", encoding="utf-8") as f:
    orig = f.read()

sources_idx = orig.find("export const MOCK_SOURCES")
sources_tail = orig[sources_idx:]
genres_end = orig.find("export const MOCK_SERIES: Series[] = [")
header = orig[:genres_end]

series_json = json.dumps(cat['series'], ensure_ascii=False, indent=2)
episodes_json = json.dumps(cat['episodes'], ensure_ascii=False, indent=2)

new_mock = f"""{header}export const MOCK_SERIES: Series[] = {series_json}

export const MOCK_EPISODES: Record<string, Episode[]> = {episodes_json}

{sources_tail}"""

with open(mock_path, "w", encoding="utf-8") as f:
    f.write(new_mock)

# Update MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["dramaapp"]
    for s in cat['series']:
        db["series"].update_one(
            {"id": s["id"]},
            {"$set": {"genres": s["genres"], "sourceName": s["sourceName"], "sourceId": "dramavivo"}}
        )
    print("MongoDB updated!")
except Exception as e:
    print(f"Mongo warning: {e}")

print("Scrub completed! 0 platform names in genres.")
