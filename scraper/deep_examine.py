import httpx
import json
import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

print("=== DEEP EXAMINING GOODSHORT __INITIAL_STATE__ ===")
goodshort_url = "https://www.goodshort.com/drama/blood-and-bones-of-the-disowned-daughter-31001113972"
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get(goodshort_url)
    m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', r.text)
    if m:
        state_json = m.group(1)
        data = json.loads(state_json)
        print("Initial state top keys:", list(data.keys()))
        for k, v in data.items():
            if isinstance(v, dict):
                print(f"  {k} keys:", list(v.keys())[:10])
                if "bookInfo" in v or "chapter" in v or "drama" in v or "playlet" in v:
                    print(f"  --> {k}:", str(v)[:300])
            elif isinstance(v, list) and len(v) > 0:
                print(f"  {k} (list len {len(v)}):", str(v[0])[:150])

print("\n=== DEEP EXAMINING NETSHORT EPISODE PAGE ===")
netshort_url = "https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521"
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get(netshort_url)
    # Check all scripts and chunks
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', r.text)
    print("Found chunks:", len(chunks))
    combined = ""
    for c in chunks:
        try:
            combined += json.loads(f'"{c}"')
        except Exception:
            combined += c
            
    # Search for keywords
    print("Length of combined chunks:", len(combined))
    keywords = ["episode", "video", "play", "chapter", "cover", "drama", "title", "url"]
    for kw in ["shortPlay", "videoInfo", "episodeList", "currentEpisode", "playUrl", "m3u8", "videoKey", "vod"]:
        matches = [m.start() for m in re.finditer(kw, combined, re.IGNORECASE)]
        print(f"Keyword '{kw}' count: {len(matches)}")
        if matches:
            for idx in matches[:3]:
                snippet = combined[max(0, idx-50):min(len(combined), idx+150)]
                print(f"   [{kw} snippet]:", snippet.replace("\n", " "))
