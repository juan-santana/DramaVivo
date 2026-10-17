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

print("=== INSPECTING DRAMABOX ===")
try:
    with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
        r = client.get("https://www.dramabox.com/es")
        print("DramaBox status:", r.status_code)
        print("DramaBox final URL:", r.url)
        soup = BeautifulSoup(r.text, "html.parser")
        print("Title:", soup.title.string if soup.title else "No title")
        
        # Check __NEXT_DATA__, __NUXT__, __INITIAL_STATE__
        for s in soup.find_all("script"):
            sid = s.get("id", "")
            stype = s.get("type", "")
            if sid == "__NEXT_DATA__":
                print("Found __NEXT_DATA__!")
                data = json.loads(s.string)
                print("Keys:", list(data.keys()))
                if "props" in data:
                    print("pageProps keys:", list(data["props"].get("pageProps", {}).keys()))
            elif "application/json" in stype:
                print(f"JSON script id='{sid}' type='{stype}' len={len(s.string or '')}")
            text = s.string or ""
            if "window.__INITIAL_STATE__" in text:
                print("Found window.__INITIAL_STATE__!")
            elif "window.__NUXT__" in text:
                print("Found window.__NUXT__!")
            elif "self.__next_f" in text:
                print("Found Next.js App Router chunks!")

        # Check links
        links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
        print(f"Total links: {len(links)}")
        drama_links = [l for l in links if any(k in l for k in ["/drama", "/series", "/watch", "/detail", "/play", "/video", "/film"])]
        print("Drama links:", drama_links[:15])
        
        # Scripts
        scripts = [s.get("src") for s in soup.find_all("script") if s.get("src")]
        print("Script srcs:", len(scripts))
        for src in scripts[:8]:
            print("  Script:", src[:100])
            
except Exception as e:
    print("DramaBox error:", e)
