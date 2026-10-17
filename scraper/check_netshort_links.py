import httpx
import json
import re
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

print("=== CHECKING EXACT EPISODE URLS ON HOMEPAGES ===")
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    # 1. English
    r_en = client.get("https://netshort.com/")
    soup_en = BeautifulSoup(r_en.text, "html.parser")
    en_links = [a["href"] for a in soup_en.find_all("a", href=True) if "/episode/" in a["href"]]
    print("EN episode links found:", len(en_links))
    for l in list(set(en_links))[:10]:
        print("  EN Link:", l)

    # 2. Spanish
    r_es = client.get("https://netshort.com/es/")
    soup_es = BeautifulSoup(r_es.text, "html.parser")
    es_links = [a["href"] for a in soup_es.find_all("a", href=True) if "/episode/" in a["href"]]
    print("\nES episode links found:", len(es_links))
    for l in list(set(es_links))[:10]:
        print("  ES Link:", l)
