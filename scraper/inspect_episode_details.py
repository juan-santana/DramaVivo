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

print("=== NETSHORT: initialCurrentEpisodeInfo & Episode List ===")
netshort_url = "https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521"
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get(netshort_url)
    m = re.search(r'"initialCurrentEpisodeInfo":\s*(\{.*?\})\s*,\s*"', r.text)
    if m:
        print("initialCurrentEpisodeInfo:", m.group(1)[:500])
    else:
        # Search for where initialCurrentEpisodeInfo is
        idx = r.text.find("initialCurrentEpisodeInfo")
        print("Snippet around initialCurrentEpisodeInfo:", r.text[idx:idx+800])
        
    # Also find where video url or player src is rendered
    idx_ep = r.text.find('"episodeList"')
    if idx_ep != -1:
        print("Snippet around episodeList:", r.text[idx_ep:idx_ep+800])

print("\n=== GOODSHORT: BookInfoModule['book'] & chapters ===")
goodshort_url = "https://www.goodshort.com/drama/blood-and-bones-of-the-disowned-daughter-31001113972"
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get(goodshort_url)
    m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', r.text)
    if m:
        state = json.loads(m.group(1))
        book_info = state.get("BookInfoModule", {})
        book = book_info.get("book", {})
        print("Book title:", book.get("bookName"))
        print("Book cover:", book.get("cover"))
        print("Book introduction:", book.get("introduction")[:200] if book.get("introduction") else None)
        print("Book total chapter:", book.get("totalChapterCount"))
        print("Book tags:", book.get("tags"))
        
        chapters = book_info.get("chapterVoList", [])
        print("Chapters count:", len(chapters))
        if chapters:
            print("Sample chapter 0:", chapters[0])
            first_ch_id = chapters[0].get("id")
            # Let's check if there's a chapter watch URL or playback endpoint
            print("First chapter id/resource:", first_ch_id, chapters[0].get("chapterResourceUrl"))
