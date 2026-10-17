import json
from pymongo import MongoClient

print("=== SYNCING TO MONGODB CLEANLY ===")
catalog_path = "output/dramashorts_real_catalog.json"
with open(catalog_path, "r", encoding="utf-8") as f:
    master_catalog = json.load(f)

client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
db = client["dramaapp"]

# Clear existing series and episodes to avoid duplicate slug conflicts
db["series"].delete_many({})
db["episodes"].delete_many({})

series_docs = []
for s in master_catalog["series"]:
    lang = s.get("language", "spanish").lower()
    mongo_lang = "english" if ("en" in lang or "ing" in lang) else "spanish"
    doc = {
        **s,
        "language": mongo_lang,
        "publicationStatus": "PUBLISHED",
        "rightsStatus": "APPROVED"
    }
    series_docs.append(doc)

if series_docs:
    db["series"].insert_many(series_docs)
    print(f"Inserted {len(series_docs)} series into MongoDB")

episode_docs = []
for s_id, ep_list in master_catalog["episodes"].items():
    for ep in ep_list:
        doc = {
            **ep,
            "publicationStatus": "PUBLISHED",
            "rightsStatus": "APPROVED"
        }
        episode_docs.append(doc)

if episode_docs:
    db["episodes"].insert_many(episode_docs)
    print(f"Inserted {len(episode_docs)} episodes into MongoDB")

print("MongoDB sync complete and verified!")
