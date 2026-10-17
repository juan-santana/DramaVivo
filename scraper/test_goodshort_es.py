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

print("=== CHECKING GOODSHORT SPANISH: /dramas/obras ===")
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get("https://www.goodshort.com/dramas/obras")
    soup = BeautifulSoup(r.text, "html.parser")
    drama_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/drama/") and href not in drama_links:
            drama_links.append(href)
            
    print(f"Found {len(drama_links)} Spanish drama links on /dramas/obras:")
    for link in drama_links[:5]:
        print(" ", link)
        url = f"https://www.goodshort.com{link}"
        resp = client.get(url)
        m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', resp.text)
        if m:
            state = json.loads(m.group(1))
            book = state.get("BookInfoModule", {}).get("book", {})
            print(f"  Title: {book.get('bookName')} | Cover: {book.get('cover')[:60]}...")
