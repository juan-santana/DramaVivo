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

print("=== NETSHORT /es/ ===")
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get("https://netshort.com/es/")
    print("NetShort /es/ status:", r.status_code)
    # Extract all chunks of self.__next_f
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', r.text)
    print("Found next_f chunks:", len(chunks))
    full_data_str = ""
    for c in chunks:
        # unescape json string
        try:
            decoded = json.loads(f'"{c}"')
            full_data_str += decoded
        except Exception:
            full_data_str += c
    
    # Search for shortPlay objects or titles
    matches = re.findall(r'\{[^{}]*?"shortPlayId"[^{}]*?\}', full_data_str)
    print("ShortPlay objects found in /es/:", len(matches))
    for m in matches[:5]:
        print("Sample shortplay:", m[:200])

    # Check a specific drama link from NetShort
    soup = BeautifulSoup(r.text, "html.parser")
    all_links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
    print("Sample links on /es/:", [l for l in all_links if "/es/" in l or "drama" in l][:10])

print("\n=== GOODSHORT /dramas/playlets ===")
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get("https://www.goodshort.com/dramas/playlets")
    print("GoodShort /dramas/playlets status:", r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")
    links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
    print("Links on playlets page:", len(links))
    drama_links = [l for l in links if any(k in l for k in ["/drama-detail", "/detail", "/play", "/video", "/drama/"])]
    print("Drama links:", drama_links[:10])
    # Also check any link that looks like a drama
    print("First 15 links:", links[:15])
