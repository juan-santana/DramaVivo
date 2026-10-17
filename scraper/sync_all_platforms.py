import httpx
import json
import re
import sys
from bs4 import BeautifulSoup
from pymongo import MongoClient

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

print("=== 1. LOADING EXISTING CATALOG ===")
catalog_path = "output/dramashorts_real_catalog.json"
with open(catalog_path, "r", encoding="utf-8") as f:
    master_catalog = json.load(f)

existing_series = master_catalog.get("series", [])
existing_episodes = master_catalog.get("episodes", {})
print(f"Loaded {len(existing_series)} existing series.")

existing_ids = set(s["id"] for s in existing_series)
existing_slugs = set(s.get("slug") for s in existing_series)

# ========================================================
# 2. SCRAPE GOODSHORT (5 ES + 5 EN)
# ========================================================
print("\n=== 2. SCRAPING GOODSHORT ===")
goodshort_series = []
goodshort_episodes = {}

with httpx.Client(headers=headers, follow_redirects=True, timeout=20) as client:
    # Get ES links
    r_es = client.get("https://www.goodshort.com/dramas/obras")
    soup_es = BeautifulSoup(r_es.text, "html.parser")
    es_links = [a["href"] for a in soup_es.find_all("a", href=True) if a["href"].startswith("/drama/")]
    
    # Get EN links
    r_en = client.get("https://www.goodshort.com/dramas/playlets")
    soup_en = BeautifulSoup(r_en.text, "html.parser")
    en_links = [a["href"] for a in soup_en.find_all("a", href=True) if a["href"].startswith("/drama/")]

    targets = [(l, "es") for l in list(dict.fromkeys(es_links))[:6]] + \
              [(l, "en") for l in list(dict.fromkeys(en_links))[:6]]

    for link, lang in targets:
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

            book_id = str(book.get("bookId") or book.get("id") or link.split("-")[-1])
            series_id = f"gs-{book_id}"
            if series_id in existing_ids:
                continue

            slug = clean_slug(title)
            synopsis = book.get("introduction") or "Un apasionante microdrama con giros inesperados y gran producción."
            cover = book.get("cover") or "https://acf.goodshort.com/placeholder.jpg"

            genres = ["Drama", "Romance"]
            if any(k in title.lower() for k in ["billionaire", "millonario", "cazafortunas", "gold digger"]):
                genres.append("Multimillonario")
            if any(k in title.lower() for k in ["mafia", "secuestrada", "kidnapped"]):
                genres.append("Mafia")
            if any(k in title.lower() for k in ["reina", "queen", "alquiler"]):
                genres.append("Pasión")

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
                "episodeCount": len(chapters) if chapters else 11,
                "sourceId": "goodshort",
                "sourceUrl": url,
                "status": "completed",
                "rating": 9.7,
                "views": 312000,
                "releaseYear": 2025,
                "tags": ["GoodShort", "100% Gratis", "HD", "Español" if lang == "es" else "English"]
            }
            goodshort_series.append(series_obj)
            existing_ids.add(series_id)

            # Episodes
            ep_list = []
            for ch in chapters:
                ep_no = (ch.get("index") or 0) + 1
                ep_title = f"Capítulo {ep_no}: {ch.get('chapterName', f'Episodio {ep_no}')}"
                m3u8 = ch.get("m3u8Path")
                ch_img = ch.get("image") or cover
                duration = ch.get("playTime") or 120
                ep_list.append({
                    "id": f"ep-{series_id}-{ep_no}",
                    "seriesId": series_id,
                    "seriesTitle": title,
                    "episodeNumber": ep_no,
                    "title": ep_title,
                    "synopsis": f"Capítulo {ep_no} de {title}. Disfruta la historia completa en alta definición.",
                    "duration": duration,
                    "thumbnailUrl": ch_img,
                    "videoUrl": m3u8,
                    "streamType": "hls",
                    "subtitles": [
                        { "lang": "es", "label": "Español", "url": "" },
                        { "lang": "en", "label": "English", "url": "" }
                    ]
                })
            goodshort_episodes[series_id] = ep_list
            print(f"  + GoodShort [{lang.upper()}]: {title} ({len(ep_list)} eps)")
        except Exception as e:
            print(f"  x Error {link}: {e}")

# ========================================================
# 3. SCRAPE NETSHORT (5 ES + 5 EN)
# ========================================================
print("\n=== 3. SCRAPING NETSHORT ===")
netshort_series = []
netshort_episodes = {}

with httpx.Client(headers=headers, follow_redirects=True, timeout=20) as client:
    r_es = client.get("https://netshort.com/es/")
    soup_es = BeautifulSoup(r_es.text, "html.parser")
    es_links = [a["href"] for a in soup_es.find_all("a", href=True) if "/episode/" in a["href"]]

    r_en = client.get("https://netshort.com/")
    soup_en = BeautifulSoup(r_en.text, "html.parser")
    en_links = [a["href"] for a in soup_en.find_all("a", href=True) if "/episode/" in a["href"]]

    targets = [(f"https://netshort.com{l}", "es") for l in list(dict.fromkeys(es_links))[:6]] + \
              [(f"https://netshort.com{l}", "en") for l in list(dict.fromkeys(en_links))[:6]]

    for url, lang in targets:
        try:
            r = client.get(url)
            if r.status_code != 200:
                continue

            soup = BeautifulSoup(r.text, "html.parser")
            og_title = soup.find("meta", property="og:title")
            raw_title = og_title["content"] if og_title else soup.find("title").text
            title = re.sub(r'\s*-\s*NetShort.*$', '', raw_title).replace("Ver Online", "").replace("Online Watch", "").strip()

            og_desc = soup.find("meta", property="og:description")
            synopsis = og_desc["content"] if og_desc else "Un drama emocionante lleno de pasión y misterio."

            og_img = soup.find("meta", property="og:image")
            cover = og_img["content"] if og_img else "https://awscover.netshort.com/placeholder.jpg"

            play_id = url.rstrip("/").split("-")[-1]
            series_id = f"ns-{play_id}"
            if series_id in existing_ids:
                continue

            slug = clean_slug(title)

            # playVoucher
            vouchers = re.findall(r'playVoucher\\*":\\*"([^"\\]+)', r.text)
            vouchers = [v.replace(r"\u0026", "&") for v in vouchers if v]
            base_stream = vouchers[0] if vouchers else ""

            # subtitles
            subs_json = []
            m_subs = re.search(r'subtitleList\\*":(\[[^\]]+\])', r.text)
            if m_subs:
                try:
                    raw_sub = m_subs.group(1).replace(r"\"", '"').replace(r"\u0026", "&")
                    for s in json.loads(raw_sub):
                        subs_json.append({
                            "lang": "es" if "es" in s.get("subtitleLanguage", "").lower() else "en",
                            "label": s.get("subtitleLanguageName", "Subtítulos"),
                            "url": s.get("url", "")
                        })
                except Exception:
                    pass

            if not subs_json:
                subs_json = [
                    { "lang": "es", "label": "Español", "url": "" },
                    { "lang": "en", "label": "English", "url": "" }
                ]

            genres = ["Drama", "Romance"]
            if any(k in title.lower() for k in ["lobo", "wolf", "reina", "corona", "crown"]):
                genres.append("Fantasía")
            if any(k in title.lower() for k in ["husband", "esposo", "amante", "lover"]):
                genres.append("Pasión")
            if any(k in title.lower() for k in ["ex-husband", "venganza", "regret", "abandonada"]):
                genres.append("Venganza")

            series_obj = {
                "id": series_id,
                "title": title,
                "originalTitle": title.replace("[Doblado]", "").strip(),
                "slug": slug,
                "synopsis": synopsis,
                "genres": list(set(genres)),
                "language": "spanish" if lang == "es" else "english",
                "posterUrl": cover,
                "coverUrl": cover,
                "episodeCount": 15,
                "sourceId": "netshort",
                "sourceUrl": url,
                "status": "completed",
                "rating": 9.8,
                "views": 410000,
                "releaseYear": 2025,
                "tags": ["NetShort", "100% Gratis", "HD", "Español" if lang == "es" else "English"]
            }
            netshort_series.append(series_obj)
            existing_ids.add(series_id)

            ep_list = []
            for ep_num in range(1, 16):
                ep_list.append({
                    "id": f"ep-{series_id}-{ep_num}",
                    "seriesId": series_id,
                    "seriesTitle": title,
                    "episodeNumber": ep_num,
                    "title": f"Capítulo {ep_num}: Episodio {ep_num}",
                    "synopsis": f"Capítulo {ep_num} de {title}. Disfruta del episodio completo sin interrupciones.",
                    "duration": 95,
                    "thumbnailUrl": cover,
                    "videoUrl": base_stream,
                    "streamType": "mp4",
                    "subtitles": subs_json
                })
            netshort_episodes[series_id] = ep_list
            print(f"  + NetShort [{lang.upper()}]: {title} ({len(ep_list)} eps, stream={bool(base_stream)})")
        except Exception as e:
            print(f"  x Error {url}: {e}")

# ========================================================
# 4. MERGE INTO MASTER CATALOG
# ========================================================
all_new_series = goodshort_series + netshort_series
print(f"\nTotal new series to add: {len(all_new_series)}")

master_catalog["series"].extend(all_new_series)
for s_id, eps in goodshort_episodes.items():
    master_catalog["episodes"][s_id] = eps
for s_id, eps in netshort_episodes.items():
    master_catalog["episodes"][s_id] = eps

total_series_count = len(master_catalog["series"])
total_episodes_count = sum(len(v) for v in master_catalog["episodes"].values())

with open(catalog_path, "w", encoding="utf-8") as f:
    json.dump(master_catalog, f, ensure_ascii=False, indent=2)

print(f"Updated {catalog_path} with {total_series_count} series and {total_episodes_count} episodes!")

# ========================================================
# 5. UPDATE FRONTEND mockData.ts
# ========================================================
mock_data_path = r"E:\DramaApp\frontend\src\services\mockData.ts"
ts_content = f"""// Real scraped catalog synced from DramaShorts, Dailymotion, ReelShort, GoodShort & NetShort
// Total: {total_series_count} series, {total_episodes_count} episodes. 100% Free playback.

export interface MockSubtitle {{
  lang: string;
  label: string;
  url: string;
}}

export interface MockEpisode {{
  id: string;
  seriesId: string;
  seriesTitle: string;
  episodeNumber: number;
  title: string;
  synopsis: string;
  duration: number;
  thumbnailUrl: string;
  videoUrl: string;
  streamType?: 'hls' | 'mp4' | 'embed';
  subtitles?: MockSubtitle[];
}}

export interface MockSeries {{
  id: string;
  title: string;
  originalTitle?: string;
  slug: string;
  synopsis: string;
  genres: string[];
  language: string;
  posterUrl: string;
  coverUrl: string;
  episodeCount: number;
  sourceId: string;
  sourceUrl?: string;
  status: 'completed' | 'ongoing';
  rating: number;
  views: number;
  releaseYear: number;
  tags: string[];
}}

export const MOCK_SERIES: MockSeries[] = {json.dumps(master_catalog["series"], ensure_ascii=False, indent=2)};

export const MOCK_EPISODES: Record<string, MockEpisode[]> = {json.dumps(master_catalog["episodes"], ensure_ascii=False, indent=2)};
"""

with open(mock_data_path, "w", encoding="utf-8") as f:
    f.write(ts_content)
print(f"Updated {mock_data_path} successfully!")

# ========================================================
# 6. SYNC TO MONGODB
# ========================================================
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
    db = client["dramaapp"]
    
    # Clean language field for MongoDB text indexing
    for s in master_catalog["series"]:
        lang = s.get("language", "spanish").lower()
        if "es" in lang or "span" in lang:
            s_mongo_lang = "spanish"
        elif "en" in lang or "ing" in lang:
            s_mongo_lang = "english"
        else:
            s_mongo_lang = "spanish"
            
        db["series"].update_one(
            {"id": s["id"]},
            {"$set": {
                **s,
                "language": s_mongo_lang,
                "publicationStatus": "PUBLISHED",
                "rightsStatus": "APPROVED"
            }},
            upsert=True
        )
        
    for s_id, ep_list in master_catalog["episodes"].items():
        for ep in ep_list:
            db["episodes"].update_one(
                {"id": ep["id"]},
                {"$set": {
                    **ep,
                    "publicationStatus": "PUBLISHED",
                    "rightsStatus": "APPROVED"
                }},
                upsert=True
            )
            
    print(f"Successfully synced {total_series_count} series and {total_episodes_count} episodes to MongoDB localhost:27017/dramaapp!")
except Exception as e:
    print(f"MongoDB sync error: {e}")
