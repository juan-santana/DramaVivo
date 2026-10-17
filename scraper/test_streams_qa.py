import json
import httpx
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Test StardustTV streams
from extract_all_stardust import extract_all
stardust_list = extract_all()

print(f"\nTesting first 5 StardustTV streams:")
client = httpx.Client(timeout=10, follow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
for s in stardust_list[:5]:
    url = s.get('filepath')
    if url:
        try:
            r = client.head(url)
            print(f"  [{s['id']}] Status: {r.status_code} for {url[:60]}...")
        except Exception as e:
            print(f"  [{s['id']}] Error: {e} for {url[:60]}...")

# 2. Check current catalog streams
data = json.load(open('E:/DramaApp/scraper/output/dramashorts_real_catalog.json', encoding='utf-8'))
episodes = data.get('episodes', {})

sample_urls = []
for sid, eps in list(episodes.items())[:10]:
    if eps and eps[0].get('videoUrl'):
        sample_urls.append((sid, eps[0]['videoUrl']))

print(f"\nTesting 10 sample streams from current catalog:")
for sid, url in sample_urls:
    try:
        r = client.head(url)
        print(f"  [{sid}] Status: {r.status_code} for {url[:60]}...")
    except Exception as e:
        print(f"  [{sid}] Error: {e} for {url[:60]}...")
