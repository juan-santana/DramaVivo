import httpx
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://netshort.com",
    "Referer": "https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521",
}

# In page.js, let's find how /web/v4/short_play/episode_info is called
with httpx.Client(timeout=15) as client:
    resp = client.get("https://netshort.com/_next/static/chunks/app/%5Blocale%5D/episode/%5Bepisode%5D/page-1c1217f311686ba2.js")
    idx = resp.text.find("/web/v4/short_play/episode_info")
    print("Call context:", resp.text[max(0, idx-100):min(len(resp.text), idx+300)])

# Let's test calling this API
with httpx.Client(headers=headers, timeout=15) as client:
    # We have episodeId: "2105528500257710083" and shortPlayId: "2104831753981931521"
    payload = {
        "episodeId": "2105528500387733508", # Episode 2!
        "shortPlayId": "2104831753981931521",
        "language": "es_ES"
    }
    r = client.post("https://netshort.com/web/v4/short_play/episode_info", json=payload)
    print("API status:", r.status_code)
    print("API response:", r.text[:500])
    
    # Try GET as well
    r_get = client.get("https://netshort.com/web/v4/short_play/episode_info", params=payload)
    print("GET status:", r_get.status_code, "resp:", r_get.text[:300])
