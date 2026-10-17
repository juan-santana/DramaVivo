import httpx
import json
import re
import sys
import uuid
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

def clean_slug(title):
    s = title.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s).strip('-')
    return s[:60]

print("=== STARTING GOODSHORT SCRAPER ===")
goodshort_series_list = []
goodshort_episodes_dict = {}

with httpx.Client(headers=headers, follow_redirects=True, timeout=20) as client:
    # 1. English GoodShort dramas
    r_en = client.get("https://www.goodshort.com/dramas/playlets")
    soup_en = BeautifulSoup(r_en.text, "html.parser")
    en_links = []
    for a in soup_en.find_all("a", href=True):
        h = a["href"]
        if h.startswith("/drama/") and h not in en_links:
            en_links.append(h)
            
    # 2. Spanish GoodShort dramas
    r_es = client.get("https://www.goodshort.com/dramas/obras")
    soup_es = BeautifulSoup(r_es.text, "html.parser")
    es_links = []
    for a in soup_es.find_all("a", href=True):
        h = a["href"]
        if h.startswith("/drama/") and h not in es_links:
            es_links.append(h)

    print(f"Found {len(en_links)} EN links and {len(es_links)} ES links on GoodShort")

    all_goodshort_targets = []
    for l in es_links[:6]:
        all_goodshort_targets.append((l, "es"))
    for l in en_links[:6]:
        all_goodshort_targets.append((l, "en"))

    for link, lang in all_goodshort_targets:
        url = f"https://www.goodshort.com{link}"
        try:
            resp = client.get(url)
            m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', resp.text)
            if not m:
                continue
            state = json.loads(m.group(1))
            book = state.get("BookInfoModule", {}).get("book", {})
            chapters = state.get("BookInfoModule", {}).get("chapterVoList", [])
            
            title = book.get("bookName")
            if not title:
                continue
                
            book_id = str(book.get("bookId") or book.get("id") or clean_slug(title))
            series_id = f"gs-{book_id}"
            slug = clean_slug(title)
            
            synopsis = book.get("introduction") or "Un drama cautivador lleno de emoción, romance y giros inesperados."
            cover = book.get("cover") or "https://acf.goodshort.com/videobook/202509/cover-eYCOTZ5w9r.jpg"
            
            # Genres
            genres = ["Drama", "Romance"]
            if "billionaire" in title.lower() or "millonario" in title.lower():
                genres.append("Multimillonario")
            if "mafia" in title.lower():
                genres.append("Mafia")
            if "revenge" in title.lower() or "venganza" in title.lower():
                genres.append("Venganza")
            if "reina" in title.lower() or "queen" in title.lower():
                genres.append("Poder")

            original_title = title
            if lang == "es" and "[Doblado]" in title:
                original_title = title.replace("[Doblado]", "").strip()

            series_obj = {
                "id": series_id,
                "title": title,
                "originalTitle": original_title,
                "slug": slug,
                "synopsis": synopsis,
                "genres": list(set(genres)),
                "language": "spanish" if lang == "es" else "english",
                "posterUrl": cover,
                "coverUrl": cover,
                "episodeCount": len(chapters) if chapters else 12,
                "sourceId": "goodshort",
                "sourceUrl": url,
                "status": "completed",
                "rating": 9.6,
                "views": 284000,
                "releaseYear": 2025,
                "tags": ["GoodShort", "Exclusivo", "100% Gratis", "HD", "Español" if lang == "es" else "English"]
            }
            goodshort_series_list.append(series_obj)
            
            # Episodes
            ep_list = []
            for ch in chapters:
                ep_no = (ch.get("index") or 0) + 1
                ep_title = f"Capítulo {ep_no}: {ch.get('chapterName', f'Episodio {ep_no}')}"
                m3u8 = ch.get("m3u8Path")
                ch_img = ch.get("image") or cover
                duration = ch.get("playTime") or 120
                
                ep_obj = {
                    "id": f"ep-{series_id}-{ep_no}",
                    "seriesId": series_id,
                    "seriesTitle": title,
                    "episodeNumber": ep_no,
                    "title": ep_title,
                    "synopsis": f"Capítulo {ep_no} de {title}. Disfruta de toda la intensidad y emoción completa en alta calidad.",
                    "duration": duration,
                    "thumbnailUrl": ch_img,
                    "videoUrl": m3u8,
                    "streamType": "hls",
                    "subtitles": [
                        { "lang": "es", "label": "Español", "url": "" },
                        { "lang": "en", "label": "English", "url": "" }
                    ]
                }
                ep_list.append(ep_obj)
                
            goodshort_episodes_dict[series_id] = ep_list
            print(f"Scraped GoodShort [{lang.upper()}]: {title} ({len(ep_list)} episodes)")
        except Exception as e:
            print(f"Error scraping GoodShort {link}: {e}")

print(f"\nGoodShort Scraped: {len(goodshort_series_list)} series")
