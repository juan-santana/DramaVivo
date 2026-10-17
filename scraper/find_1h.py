import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('E:/DramaApp/scraper/output/dramashorts_real_catalog.json', encoding='utf-8'))
series = data.get('series', [])
print(f"Total series: {len(series)}")

one_hour = [
    s for s in series 
    if 'Series Completas (1h+)' in s.get('genres', []) 
    or 'dailymotion' in s.get('sourceId', '').lower() 
    or s.get('durationPerEpisode', 0) >= 1800
]

print(f"1h series count: {len(one_hour)}")
for s in one_hour:
    print(f"- [{s['id']}] {s['title']} | Duration: {s.get('durationPerEpisode')}s | Source: {s.get('sourceId')} | Genres: {s.get('genres')}")
