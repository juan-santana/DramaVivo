import json
import httpx
import sys

sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('E:/DramaApp/scraper/output/dramashorts_real_catalog.json', encoding='utf-8'))
episodes = data.get('episodes', {})

client = httpx.Client(timeout=8, follow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})

for prefix in ['rs', 'gs', 'ns', 'db']:
    # Find first series of this prefix
    sample_sid = None
    for sid in episodes:
        if sid.startswith(prefix + '-'):
            sample_sid = sid
            break
    if sample_sid and episodes[sample_sid]:
        first_ep = episodes[sample_sid][0]
        url = first_ep.get('videoUrl')
        print(f"Prefix {prefix} sample series {sample_sid}:")
        print(f"  URL: {url}")
        if url.startswith('http'):
            try:
                r = client.head(url)
                print(f"  Status: {r.status_code}")
            except Exception as e:
                print(f"  Error: {e}")
        elif url.startswith('/cdn-proxy'):
            print("  Vite proxy path")
