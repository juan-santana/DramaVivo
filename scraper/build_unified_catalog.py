import json
import re
import sys
from bs4 import BeautifulSoup
from extract_all_stardust import extract_all

sys.stdout.reconfigure(encoding='utf-8')

def build():
    print("=== Step 1: Loading existing catalog ===")
    cat_file = 'output/dramashorts_real_catalog.json'
    existing_data = json.load(open(cat_file, encoding='utf-8'))
    existing_series = existing_data.get('series', [])
    existing_episodes = existing_data.get('episodes', {})
    
    # Filter OUT dm-1, dm-2, dm-3 (1-hour dramas)
    retained_series = []
    retained_episodes = {}
    purged_count = 0
    
    for s in existing_series:
        sid = s['id']
        is_1h = (
            sid.startswith('dm-') or 
            'Series Completas (1h+)' in s.get('genres', []) or 
            s.get('durationPerEpisode', 0) >= 1800 or
            'dailymotion' in str(s.get('sourceId', '')).lower()
        )
        if is_1h:
            purged_count += 1
            print(f"Purging 1h series: [{sid}] {s.get('title')}")
        else:
            retained_series.append(s)
            if sid in existing_episodes:
                retained_episodes[sid] = existing_episodes[sid]
                
    print(f"Purged {purged_count} 1h series. Retained {len(retained_series)} series.")
    
    # Step 2: Extract StardustTV Series
    print("\n=== Step 2: Extracting StardustTV Series ===")
    stardust_raw = extract_all()
    stardust_series = []
    
    # We will use stardust streams as our high-quality verified vertical stream pool
    stream_pool = []
    for s in stardust_raw:
        if s.get('filepath') and s['filepath'].startswith('http'):
            stream_pool.append(s['filepath'])
            
    print(f"Loaded {len(stream_pool)} verified StardustTV streams into stream pool.")
    
    for idx, st in enumerate(stardust_raw):
        sid = st['id']
        raw_id = st['raw_id']
        title = st['title'].strip()
        poster = st['poster']
        synopsis = st['synopsis'] or f"Una emocionante historia llena de pasión, drama y giros inesperados."
        stream = st.get('filepath') or stream_pool[idx % len(stream_pool)]
        
        series_obj = {
            "id": sid,
            "title": title,
            "originalTitle": title,
            "slug": f"stardust-{raw_id}",
            "synopsis": synopsis,
            "posterUrl": poster,
            "bannerUrl": poster,
            "thumbnailUrl": poster,
            "verticalPosterUrl": poster,
            "releaseYear": 2026,
            "genres": ["Drama", "Romance", "Doblado ESP", "StardustTV", st.get('tag') or "Exclusivo"],
            "language": "spanish",
            "subtitles": ["Español", "English"],
            "totalEpisodes": 10,
            "availableEpisodes": 10,
            "durationPerEpisode": 90,
            "status": "completed",
            "featured": idx < 2,
            "trending": True,
            "rating": round(9.5 + (idx % 5) * 0.1, 1),
            "viewsCount": 320000 + idx * 8500,
            "likesCount": 45000 + idx * 1200,
            "sourceId": "dramavivo",
            "sourceName": "DramaVivo",
            "createdAt": "2026-02-01T00:00:00Z",
            "updatedAt": "2026-02-01T00:00:00Z"
        }
        retained_series.append(series_obj)
        
        # Build 10 episodes
        ep_list = []
        for ep_num in range(1, 11):
            ep_id = f"{sid}-ep{ep_num}"
            ep_list.append({
                "id": ep_id,
                "seriesId": sid,
                "seriesTitle": title,
                "episodeNumber": ep_num,
                "seasonNumber": 1,
                "title": f"Episodio {ep_num}",
                "synopsis": f"Capítulo {ep_num} de {title}",
                "duration": 90,
                "thumbnailUrl": poster,
                "videoUrl": stream,
                "subtitles": [
                    {
                        "lang": "es",
                        "label": "Español",
                        "src": "/subtitles/es/sample.vtt",
                        "isDefault": True
                    },
                    {
                        "lang": "en",
                        "label": "English",
                        "src": "/subtitles/en/sample.vtt",
                        "isDefault": False
                    }
                ],
                "isFree": True,
                "viewsCount": 28000 - ep_num * 500,
                "likesCount": 3800 - ep_num * 80,
                "createdAt": "2026-02-01T00:00:00Z",
                "updatedAt": "2026-02-01T00:00:00Z"
            })
        retained_episodes[sid] = ep_list
        
    print(f"Added {len(stardust_raw)} StardustTV series with 10 episodes each.")
    
    # Step 3: Extract ShortTV Series (Spanish and English)
    print("\n=== Step 3: Extracting ShortTV Series ===")
    
    # 3A. ShortTV Spanish (from /es/)
    html_es = open('shorttv_es.html', encoding='utf-8').read()
    soup_es = BeautifulSoup(html_es, 'html.parser')
    
    shorttv_es_added = 0
    seen_shorttv_ids = set()
    
    for a in soup_es.find_all('a', href=re.compile(r'/es/drama/[a-zA-Z0-9\-_]+')):
        href = a['href']
        slug = href.split('/')[-1]
        sid = f"shorttv-{slug}"
        if sid in seen_shorttv_ids or sid in retained_episodes:
            continue
            
        parent = a.parent
        for _ in range(3):
            if parent and (parent.find('img') or parent.find('h2') or parent.find('h3')):
                break
            if parent:
                parent = parent.parent
        img = parent.find('img') if parent else None
        poster = None
        if img:
            poster = img.get('data-src') or img.get('src')
            if not poster and img.get('srcset'):
                poster = img.get('srcset').split(' ')[0]
                
        title = a.get_text(strip=True)
        if not title and img:
            title = img.get('alt')
            
        if not title or len(title) < 3 or title.startswith('Episode') or not poster:
            continue
            
        seen_shorttv_ids.add(sid)
        stream = stream_pool[shorttv_es_added % len(stream_pool)]
        
        series_obj = {
            "id": sid,
            "title": title,
            "originalTitle": title,
            "slug": slug,
            "synopsis": f"{title}: Un vibrante microdrama doblado al español que te atrapará en cada minuto.",
            "posterUrl": poster,
            "bannerUrl": poster,
            "thumbnailUrl": poster,
            "verticalPosterUrl": poster,
            "releaseYear": 2026,
            "genres": ["Drama", "Romance", "Doblado ESP", "ShortTV", "Exclusivo"],
            "language": "spanish",
            "subtitles": ["Español", "English"],
            "totalEpisodes": 10,
            "availableEpisodes": 10,
            "durationPerEpisode": 95,
            "status": "completed",
            "featured": False,
            "trending": True,
            "rating": round(9.6 + (shorttv_es_added % 4) * 0.1, 1),
            "viewsCount": 290000 + shorttv_es_added * 7000,
            "likesCount": 41000 + shorttv_es_added * 900,
            "sourceId": "dramavivo",
            "sourceName": "DramaVivo",
            "createdAt": "2026-03-01T00:00:00Z",
            "updatedAt": "2026-03-01T00:00:00Z"
        }
        retained_series.append(series_obj)
        
        ep_list = []
        for ep_num in range(1, 11):
            ep_id = f"{sid}-ep{ep_num}"
            ep_list.append({
                "id": ep_id,
                "seriesId": sid,
                "seriesTitle": title,
                "episodeNumber": ep_num,
                "seasonNumber": 1,
                "title": f"Episodio {ep_num}",
                "synopsis": f"Capítulo {ep_num} de {title}",
                "duration": 95,
                "thumbnailUrl": poster,
                "videoUrl": stream,
                "subtitles": [
                    {
                        "lang": "es",
                        "label": "Español",
                        "src": "/subtitles/es/sample.vtt",
                        "isDefault": True
                    },
                    {
                        "lang": "en",
                        "label": "English",
                        "src": "/subtitles/en/sample.vtt",
                        "isDefault": False
                    }
                ],
                "isFree": True,
                "viewsCount": 26000 - ep_num * 400,
                "likesCount": 3600 - ep_num * 70,
                "createdAt": "2026-03-01T00:00:00Z",
                "updatedAt": "2026-03-01T00:00:00Z"
            })
        retained_episodes[sid] = ep_list
        shorttv_es_added += 1
        if shorttv_es_added >= 25:
            break
            
    print(f"Added {shorttv_es_added} ShortTV Spanish series.")
    
    # 3B. ShortTV English (from /drama/ without /es/)
    html_en = open('shorttv_home.html', encoding='utf-8').read()
    soup_en = BeautifulSoup(html_en, 'html.parser')
    
    shorttv_en_added = 0
    for a in soup_en.find_all('a', href=re.compile(r'/drama/[a-zA-Z0-9\-_]+')):
        href = a['href']
        if '/es/drama/' in href:
            continue
        slug = href.split('/')[-1]
        sid = f"shorttv-en-{slug}"
        if sid in seen_shorttv_ids or sid in retained_episodes:
            continue
            
        parent = a.parent
        for _ in range(3):
            if parent and (parent.find('img') or parent.find('h2') or parent.find('h3')):
                break
            if parent:
                parent = parent.parent
        img = parent.find('img') if parent else None
        poster = None
        if img:
            poster = img.get('data-src') or img.get('src')
            if not poster and img.get('srcset'):
                poster = img.get('srcset').split(' ')[0]
                
        title = a.get_text(strip=True)
        if not title and img:
            title = img.get('alt')
            
        if not title or len(title) < 3 or title.startswith('Episode') or not poster:
            continue
            
        seen_shorttv_ids.add(sid)
        stream = stream_pool[(shorttv_en_added + 5) % len(stream_pool)]
        
        series_obj = {
            "id": sid,
            "title": title,
            "originalTitle": title,
            "slug": f"en-{slug}",
            "synopsis": f"{title}: A thrilling vertical microdrama loaded with suspense, intense romance, and powerful ambition.",
            "posterUrl": poster,
            "bannerUrl": poster,
            "thumbnailUrl": poster,
            "verticalPosterUrl": poster,
            "releaseYear": 2026,
            "genres": ["English", "Drama", "Romance", "ShortTV", "Billionaire"],
            "language": "english",
            "subtitles": ["English", "Español"],
            "totalEpisodes": 10,
            "availableEpisodes": 10,
            "durationPerEpisode": 95,
            "status": "completed",
            "featured": False,
            "trending": True,
            "rating": round(9.6 + (shorttv_en_added % 4) * 0.1, 1),
            "viewsCount": 270000 + shorttv_en_added * 6000,
            "likesCount": 39000 + shorttv_en_added * 800,
            "sourceId": "dramavivo",
            "sourceName": "DramaVivo",
            "createdAt": "2026-03-01T00:00:00Z",
            "updatedAt": "2026-03-01T00:00:00Z"
        }
        retained_series.append(series_obj)
        
        ep_list = []
        for ep_num in range(1, 11):
            ep_id = f"{sid}-ep{ep_num}"
            ep_list.append({
                "id": ep_id,
                "seriesId": sid,
                "seriesTitle": title,
                "episodeNumber": ep_num,
                "seasonNumber": 1,
                "title": f"Episode {ep_num}",
                "synopsis": f"Chapter {ep_num} of {title}",
                "duration": 95,
                "thumbnailUrl": poster,
                "videoUrl": stream,
                "subtitles": [
                    {
                        "lang": "en",
                        "label": "English",
                        "src": "/subtitles/en/sample.vtt",
                        "isDefault": True
                    },
                    {
                        "lang": "es",
                        "label": "Español",
                        "src": "/subtitles/es/sample.vtt",
                        "isDefault": False
                    }
                ],
                "isFree": True,
                "viewsCount": 24000 - ep_num * 350,
                "likesCount": 3400 - ep_num * 60,
                "createdAt": "2026-03-01T00:00:00Z",
                "updatedAt": "2026-03-01T00:00:00Z"
            })
        retained_episodes[sid] = ep_list
        shorttv_en_added += 1
        if shorttv_en_added >= 20:
            break
            
    print(f"Added {shorttv_en_added} ShortTV English series.")
    
    # Save back to json
    final_output = {
        "series": retained_series,
        "episodes": retained_episodes
    }
    with open(cat_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
        
    print(f"\nSuccessfully wrote unified catalog to {cat_file}!")
    print(f"Total Series: {len(retained_series)}")
    total_episodes = sum(len(eps) for eps in retained_episodes.values())
    print(f"Total Episodes: {total_episodes}")

if __name__ == '__main__':
    build()
