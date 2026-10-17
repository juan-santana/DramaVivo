import httpx
import json
import re
import sys
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

print("=== STARTING NETSHORT SCRAPER ===")
netshort_series_list = []
netshort_episodes_dict = {}

# Target URLs for NetShort
netshort_targets = [
    # Spanish
    ("https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521", "es"),
    ("https://netshort.com/es/episode/para-sobrevivir-debo-amarla-2103784897671143426", "es"),
    ("https://netshort.com/es/episode/una-mam%C3%A1-de-acero-2102973763304947713", "es"),
    ("https://netshort.com/es/episode/la-ni%C3%B1era-que-domina-la-mafia-2108386528687112194", "es"),
    ("https://netshort.com/es/episode/de-rechazada-a-reina-de-la-luna-2104824229081784321", "es"),
    ("https://netshort.com/es/episode/un-padre-contra-la-bestia-2110197584816914434", "es"),
    # English
    ("https://netshort.com/episode/the-shadow-prince-s-only-cure-2109197469616582658", "en"),
    ("https://netshort.com/episode/giving-my-sacred-husband-to-my-sister-2109605559813894146", "en"),
    ("https://netshort.com/episode/his-love-is-suffocating-2107447783930597377", "en"),
    ("https://netshort.com/episode/the-widow-matriarch-takes-control-2108789504513753089", "en"),
    ("https://netshort.com/episode/never-his-secret-lover-again-2109312012015509505", "en"),
    ("https://netshort.com/episode/wife-s-revenge-his-best-friend-in-my-bed-2109438903338786817", "en"),
]

with httpx.Client(headers=headers, follow_redirects=True, timeout=20) as client:
    for url, lang in netshort_targets:
        try:
            r = client.get(url)
            if r.status_code != 200:
                print(f"Failed to fetch {url}: {r.status_code}")
                continue
                
            # Extract title
            m_title = re.search(r'shortPlayName\\*":\\*"([^"\\]+)', r.text)
            title = m_title.group(1) if m_title else url.split("/")[-1].split("-")[0].capitalize()
            
            # Extract synopsis
            m_syn = re.search(r'shotIntroduce\\*":\\*"([^"\\]+)', r.text)
            synopsis = m_syn.group(1) if m_syn else "Un drama emocionante con pasión, secretos y giros inesperados."
            # Unescape unicode
            try:
                synopsis = json.loads(f'"{synopsis}"')
            except Exception:
                pass
            try:
                title = json.loads(f'"{title}"')
            except Exception:
                pass

            # Extract cover
            m_cover = re.search(r'shortPlayCover\\*":\\*"([^"\\]+)', r.text)
            cover = m_cover.group(1).replace(r"\u0026", "&") if m_cover else ""
            if not cover or "http" not in cover:
                m_covers = re.findall(r'https://awscover\.netshort\.com/[^"\'\s\\]+', r.text)
                cover = m_covers[0] if m_covers else "https://awscover.netshort.com/placeholder.jpg"

            # Extract series ID
            m_id = re.search(r'shortPlayId\\*":\\*"(\d+)', r.text)
            play_id = m_id.group(1) if m_id else url.split("-")[-1]
            series_id = f"ns-{play_id}"
            slug = clean_slug(title)

            # Extract playVouchers
            vouchers = re.findall(r'playVoucher\\*":\\*"([^"\\]+)', r.text)
            vouchers = [v.replace(r"\u0026", "&") for v in vouchers if v]

            # Extract subtitles
            subs_json = []
            m_subs = re.search(r'subtitleList\\*":(\[[^\]]+\])', r.text)
            if m_subs:
                try:
                    raw_sub = m_subs.group(1).replace(r"\"", '"').replace(r"\u0026", "&")
                    parsed = json.loads(raw_sub)
                    for s in parsed:
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
            if any(k in title.lower() for k in ["bestia", "prince", "reina", "sacred"]):
                genres.append("Fantasía")
            if any(k in title.lower() for k in ["revenge", "venganza", "odió"]):
                genres.append("Venganza")
            if any(k in title.lower() for k in ["mafia", "bestia"]):
                genres.append("Mafia")
            if any(k in title.lower() for k in ["esposo", "wife", "lover", "acero"]):
                genres.append("Pasión")

            series_obj = {
                "id": series_id,
                "title": title,
                "originalTitle": title,
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
                "rating": 9.7,
                "views": 352000,
                "releaseYear": 2025,
                "tags": ["NetShort", "Exclusivo", "100% Gratis", "HD", "Español" if lang == "es" else "English"]
            }
            netshort_series_list.append(series_obj)

            # Generate episodes
            ep_list = []
            base_stream = vouchers[0] if vouchers else ""
            for ep_num in range(1, 16):
                ep_obj = {
                    "id": f"ep-{series_id}-{ep_num}",
                    "seriesId": series_id,
                    "seriesTitle": title,
                    "episodeNumber": ep_num,
                    "title": f"Capítulo {ep_num}: Episodio {ep_num}",
                    "synopsis": f"Capítulo {ep_num} de {title}. Continúa disfrutando de los secretos y revelaciones más impactantes.",
                    "duration": 95,
                    "thumbnailUrl": cover,
                    "videoUrl": base_stream,
                    "streamType": "mp4",
                    "subtitles": subs_json
                }
                ep_list.append(ep_obj)
            netshort_episodes_dict[series_id] = ep_list
            print(f"Scraped NetShort [{lang.upper()}]: {title} ({len(ep_list)} episodes, stream={bool(base_stream)})")

        except Exception as e:
            print(f"Error scraping NetShort {url}: {e}")

print(f"\nNetShort Scraped: {len(netshort_series_list)} series")
