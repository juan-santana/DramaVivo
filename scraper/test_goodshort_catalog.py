import httpx
import json
import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

print("=== SCRAPING GOODSHORT DRAMA CATALOG ===")
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get("https://www.goodshort.com/dramas/playlets")
    soup = BeautifulSoup(r.text, "html.parser")
    drama_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/drama/") and href not in drama_links:
            drama_links.append(href)
            
    print(f"Found {len(drama_links)} drama links on GoodShort:")
    for link in drama_links[:10]:
        print(" ", link)
        
    # Let's inspect the first 3 dramas in detail
    for link in drama_links[:3]:
        url = f"https://www.goodshort.com{link}"
        resp = client.get(url)
        m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', resp.text)
        if m:
            state = json.loads(m.group(1))
            book = state.get("BookInfoModule", {}).get("book", {})
            chapters = state.get("BookInfoModule", {}).get("chapterVoList", [])
            print(f"\nDrama: {book.get('bookName')}")
            print(f"  Cover: {book.get('cover')}")
            print(f"  Synopsis: {book.get('introduction', '')[:120]}...")
            print(f"  Chapters available: {len(chapters)}")
            if chapters:
                print(f"  Ep 1 m3u8: {chapters[0].get('m3u8Path', '')[:80]}...")
