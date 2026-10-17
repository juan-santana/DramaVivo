import httpx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with httpx.Client(timeout=15) as client:
    resp = client.get("https://netshort.com/_next/static/chunks/app/%5Blocale%5D/episode/%5Bepisode%5D/page-1c1217f311686ba2.js")
    # Search for T =
    matches = re.findall(r'(?:var\s+T\s*=|T\s*=\s*n\(\d+\)|import\s*.*?\s*from)', resp.text)
    print("Matches for T:", matches[:10])
    # Search for (0, T.P)
    m = re.search(r'([a-zA-Z0-9_$]+)\s*=\s*n\((\d+)\);.*?(?:0,\s*\1\.P)', resp.text)
    if m:
        print("T module id:", m.group(2))
    
    # Or search for /web/v4 in all chunks
    soup_resp = client.get("https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(soup_resp.text, "html.parser")
    for s in soup.find_all("script"):
        src = s.get("src")
        if src and "/_next/" in src:
            chunk = client.get(f"https://netshort.com{src}")
            if "/web/v4/short_play" in chunk.text:
                print("Found /web/v4/short_play in chunk:", src)
            if "baseUrl" in chunk.text or "BASE_URL" in chunk.text:
                print("Found baseUrl in chunk:", src)
