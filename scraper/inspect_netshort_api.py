import httpx
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    # Test query param
    r1 = client.get("https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521?episode=2")
    m1 = re.search(r'"initialPlayEpisodeIndex":(\d+)', r1.text)
    print("Test ?episode=2 -> initialPlayEpisodeIndex:", m1.group(1) if m1 else None)
    
    r2 = client.get("https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521?episodeNo=2")
    m2 = re.search(r'"initialPlayEpisodeIndex":(\d+)', r2.text)
    print("Test ?episodeNo=2 -> initialPlayEpisodeIndex:", m2.group(1) if m2 else None)
    
    # Check if there is an API in client JS
    # Find all script src
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r1.text, "html.parser")
    for s in soup.find_all("script"):
        src = s.get("src", "")
        if "/_next/static/chunks/" in src and "app" in src or "page" in src:
            js = client.get(f"https://netshort.com{src}")
            # Search for api or fetch calls
            endpoints = re.findall(r'["\'](/api/[^"\']+)["\']', js.text)
            if endpoints:
                print("Endpoints in", src[-30:], ":", set(endpoints))
            # Also search for domain calls
            domains = re.findall(r'https?://[a-zA-Z0-9.-]+\.netshort\.com/[^"\']+', js.text)
            if domains:
                print("Domains in", src[-30:], ":", set(domains[:3]))
