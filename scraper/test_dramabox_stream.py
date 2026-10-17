import httpx
import json
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Origin": "http://localhost:5173",
    "Referer": "https://www.dramabox.com/",
}

detail_url = "https://www.dramabox.com/es/drama/41000110515/Escape-With-Boss-s-Baby"
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r_detail = client.get(detail_url)
    soup = BeautifulSoup(r_detail.text, "html.parser")
    next_tag = soup.find("script", id="__NEXT_DATA__")
    d = json.loads(next_tag.string)
    ch0 = d["props"]["pageProps"]["chapterList"][0]
    mp4_url = ch0.get("mp4")
    print("MP4 URL:", mp4_url[:120])
    
    # Check headers
    head_resp = client.head(mp4_url)
    print("MP4 HEAD Status:", head_resp.status_code)
    print("Content-Type:", head_resp.headers.get("content-type"))
    print("Content-Length:", head_resp.headers.get("content-length"))
    print("CORS Access-Control-Allow-Origin:", head_resp.headers.get("access-control-allow-origin"))

    # Also check other chapters
    unlocked_count = sum(1 for ch in d["props"]["pageProps"]["chapterList"] if ch.get("mp4"))
    print(f"Total chapters with mp4 in chapterList: {unlocked_count} of {len(d['props']['pageProps']['chapterList'])}")
