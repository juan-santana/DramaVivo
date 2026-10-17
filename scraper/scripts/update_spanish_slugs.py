import json
import re
import unicodedata

def slugify(title):
    t = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore').decode('utf-8')
    t = re.sub(r'[^a-zA-Z0-9\s-]', '', t).strip().lower()
    return re.sub(r'[\s-]+', '-', t)

with open('E:/DramaApp/scraper/output/dramashorts_real_catalog.json', 'r', encoding='utf-8') as f:
    saved = json.load(f)

series_list = saved['series']
episodes_dict = saved['episodes']

# Assign clean Spanish slugs
for s in series_list:
    spanish_slug = slugify(s['title'])
    s['slug'] = spanish_slug

# Also update episodes seriesTitle
for sid, eps in episodes_dict.items():
    s_parent = next((s for s in series_list if s['id'] == sid), None)
    if s_parent:
        for ep in eps:
            ep['seriesTitle'] = s_parent['title']

with open('E:/DramaApp/scraper/output/dramashorts_real_catalog.json', 'w', encoding='utf-8') as f:
    json.dump({'series': series_list, 'episodes': episodes_dict}, f, indent=2, ensure_ascii=False)

print("Slugs en español generados:")
for s in series_list:
    print(f"  {s['id']} -> /serie/{s['slug']} ({s['title']})")
