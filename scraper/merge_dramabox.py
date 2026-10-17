import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

catalog_path = "output/dramashorts_real_catalog.json"
dramabox_path = "output/dramabox_scraped.json"

with open(catalog_path, "r", encoding="utf-8") as f:
    master = json.load(f)

with open(dramabox_path, "r", encoding="utf-8") as f:
    db_data = json.load(f)

existing_ids = set(s["id"] for s in master["series"])

new_added = 0
for s in db_data["series"]:
    if s["id"] not in existing_ids:
        master["series"].append(s)
        existing_ids.add(s["id"])
        new_added += 1

for s_id, ep_list in db_data["episodes"].items():
    master["episodes"][s_id] = ep_list

print(f"Added {new_added} new DramaBox series.")
print(f"Total series in master: {len(master['series'])}")
print(f"Total episodes in master: {sum(len(v) for v in master['episodes'].values())}")

with open(catalog_path, "w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=2)

print("Saved updated master catalog!")
