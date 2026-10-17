import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

html = open('shorttv_home.html', encoding='utf-8').read()
payload_match = re.search(r'<script[^>]*>(\[\["ShallowReactive".*?\])</script>', html, re.DOTALL)
if payload_match:
    raw = payload_match.group(1)
    data = json.loads(raw)
    print("ShortTV payload items:", len(data))
    
    # In Nuxt 3 devalue serialization:
    # Find all strings and print those that look like titles or URLs
    titles = []
    covers = []
    video_urls = []
    
    for item in data:
        if isinstance(item, str):
            if any(ext in item for ext in ['.jpg', '.png', '.webp', '.jpeg']):
                covers.append(item)
            elif any(ext in item for ext in ['.mp4', '.m3u8']):
                video_urls.append(item)
            elif len(item) > 5 and len(item) < 80 and not item.startswith('http') and not item.startswith('/') and not item.startswith('$'):
                if any(w in item.lower() for w in ['billionaire', 'ceo', 'queen', 'mafia', 'love', 'kingpin', 'reunion', 'baby', 'wedding', 'revenge', 'war', 'destined', 'genius', 'dubbed']):
                    titles.append(item)
                    
    print(f"Titles found ({len(titles)}):", titles[:15])
    print(f"Covers found ({len(covers)}):", covers[:10])
    print(f"Videos found ({len(video_urls)}):", video_urls[:10])
    
    # Also look at objects that have keys like 'drama_name' or 'name' or 'title'
    drama_objs = []
    for item in data:
        if isinstance(item, dict):
            # Resolve keys and values if they are integer indices
            resolved = {}
            for k, v in item.items():
                k_str = data[k] if isinstance(k, int) and k < len(data) else str(k)
                resolved[k_str] = v
            if any(k in resolved for k in ['title', 'name', 'drama_name', 'cover', 'cover_path', 'intro']):
                drama_objs.append(resolved)
    print(f"Drama objects found: {len(drama_objs)}")
    if drama_objs:
        print("Sample drama object:", drama_objs[0])
