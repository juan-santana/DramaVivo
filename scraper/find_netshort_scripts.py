import httpx
import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get("https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521")
    soup = BeautifulSoup(r.text, "html.parser")
    scripts = [s.get("src") for s in soup.find_all("script") if s.get("src")]
    print("Scripts on page:", len(scripts))
    for s in scripts:
        print(" ", s)
        if "episode" in s or "page-" in s:
            url = f"https://netshort.com{s}" if s.startswith("/") else s
            resp = client.get(url)
            # Find fetch or axios calls
            calls = re.findall(r'(?:fetch|get|post)\(["\']([^"\']+)["\']', resp.text)
            print("  Calls:", calls[:10])
            # Search for api
            apis = re.findall(r'["\'](/api/[^"\']+|/gateway/[^"\']+|/v\d+/[^"\']+)["\']', resp.text)
            print("  APIs:", set(apis))
