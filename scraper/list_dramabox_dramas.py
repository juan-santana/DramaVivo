import httpx
import json
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get("https://www.dramabox.com/es")
    soup = BeautifulSoup(r.text, "html.parser")
    next_tag = soup.find("script", id="__NEXT_DATA__")
    data = json.loads(next_tag.string)
    page_props = data.get("props", {}).get("pageProps", {})
    
    big_list = page_props.get("bigList", [])
    print(f"=== BIG LIST ({len(big_list)}) ===")
    for b in big_list:
        print(f"  [{b.get('bookId')}]: {b.get('bookName')} (EN: {b.get('bookNameEn')})")
        print(f"     Cover: {b.get('cover')[:60]}... | Chapters: {b.get('chapterCount')}")
        
    small_data = page_props.get("smallData", [])
    print(f"\n=== SMALL DATA CATEGORIES ({len(small_data)}) ===")
    all_dramas = list(big_list)
    for section in small_data:
        sec_name = section.get("name")
        items = section.get("items", [])
        print(f"\nSection '{sec_name}' has {len(items)} items:")
        for it in items:
            b_id = it.get("bookId") or it.get("action")
            b_name = it.get("bookName") or it.get("name")
            print(f"   [{b_id}]: {b_name} (EN: {it.get('bookNameEn')})")
            all_dramas.append(it)
            
    print(f"\nTotal DramaBox drama items found: {len(all_dramas)}")
