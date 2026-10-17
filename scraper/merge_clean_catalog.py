import json
import re

print("=== MERGING CATALOG WITH NEW SCRAPED DRAMAS & PURGING BROKEN ONES ===")

# 1. Load main catalog
cat_path = r"E:\DramaApp\scraper\output\dramashorts_real_catalog.json"
cat = json.load(open(cat_path, encoding='utf-8'))

# 2. Load newly scraped DramaBox series
new_data = json.load(open(r"E:\DramaApp\scraper\output\dramabox_new_scraped.json", encoding='utf-8'))

# 3. Identify and purge broken series
broken_ids = {
    'ds-deep-19', 'ds-deep-20', 'ds-deep-21', 'ds-deep-22',
    'ds-deep-25', 'ds-deep-27', 'ds-deep-29', 'ds-deep-30'
}

purged_series = []
for s in cat['series']:
    sid = s['id']
    poster = s.get('posterUrl', '')
    if sid in broken_ids or 'placeholder' in poster:
        print(f"Purging broken series: {sid} - {s.get('title')}")
        if sid in cat['episodes']:
            del cat['episodes'][sid]
        continue
    # Rebrand sources to DramaVivo
    s['sourceName'] = 'DramaVivo Original' if s.get('featured') else 'DramaVivo Exclusivo'
    purged_series.append(s)

print(f"Retained {len(purged_series)} valid series from existing catalog.")

# 4. Add new scraped series
added_count = 0
for s in new_data['series']:
    sid = s['id']
    if not any(existing['id'] == sid for existing in purged_series):
        s['sourceName'] = 'DramaVivo Exclusivo'
        purged_series.append(s)
        cat['episodes'][sid] = new_data['episodes'][sid]
        added_count += 1

print(f"Added {added_count} brand new scraped series.")
print(f"Total series in new catalog: {len(purged_series)}")
print(f"Total series with episodes: {len(cat['episodes'])}")
total_eps = sum(len(eps) for eps in cat['episodes'].values())
print(f"Total playable episodes across entire catalog: {total_eps}")

# Verify no placeholders remain
for s in purged_series:
    assert 'placeholder' not in s.get('posterUrl', ''), f"Error: placeholder found in {s['id']}"

cat['series'] = purged_series

# Save updated JSON
with open(cat_path, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=2)

print("Catalog JSON updated successfully!")
