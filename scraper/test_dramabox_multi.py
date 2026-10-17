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

test_dramas = [
    ("41000106749", "Masked-Magnate-The-Dominant-Son-in-Law-DUBBED"),
    ("41000105042", "The-Divorced-Billionaire-Heiress"),
    ("41000104219", "Mafia-s-Good-Girl")
]

with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    for book_id, slug in test_dramas:
        url = f"https://www.dramabox.com/es/drama/{book_id}/{slug}"
        r = client.get(url)
        print(f"\nDrama {book_id} Status:", r.status_code)
        soup = BeautifulSoup(r.text, "html.parser")
        next_tag = soup.find("script", id="__NEXT_DATA__")
        if next_tag:
            d = json.loads(next_tag.string)
            props = d.get("props", {}).get("pageProps", {})
            book = props.get("bookInfo", {})
            chapters = props.get("chapterList", [])
            print("  Title ES:", book.get("bookName"))
            print("  Title EN:", book.get("bookNameEn"))
            print("  Cover:", book.get("cover")[:60] if book.get("cover") else None)
            print("  Total Chapters:", len(chapters))
            mp4_count = sum(1 for ch in chapters if ch.get("mp4"))
            print("  Chapters with MP4 stream:", mp4_count)
            if chapters and chapters[0].get("mp4"):
                print("  Sample MP4:", chapters[0]["mp4"][:90])
