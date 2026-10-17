import httpx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with httpx.Client(timeout=15) as client:
    resp = client.get("https://netshort.com/_next/static/chunks/app/%5Blocale%5D/episode/%5Bepisode%5D/page-1c1217f311686ba2.js")
    # Search for words like fetch, playVoucher, episodeId, or api
    print("Page js length:", len(resp.text))
    # Look for fetch patterns or strings containing /
    urls = re.findall(r'["\'](/[^"\']+)["\']', resp.text)
    print("Sample relative paths in page.js:", set([u for u in urls if len(u) > 3 and not u.startswith("/_next")][:20]))
    
    # Check mentions of playVoucher
    for m in re.finditer(r'playVoucher', resp.text):
        idx = m.start()
        print("playVoucher context:", resp.text[max(0, idx-60):min(len(resp.text), idx+140)])
