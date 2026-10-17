import re
import json
import sys
from inspect_shorttv_cards import devalue_deref

sys.stdout.reconfigure(encoding='utf-8')

html = open('sample_shorttv_drama.html', encoding='utf-8').read()
match = re.search(r'<script[^>]*>(\[\["ShallowReactive".*?\])</script>', html, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    print(f"Data length: {len(data)}")
    
    # Check for videos, episodes, streams
    streams = []
    for i, item in enumerate(data):
        if isinstance(item, str) and ('.m3u8' in item or '.mp4' in item):
            streams.append(item)
    print("Direct streams found:", len(streams))
    for s in streams[:5]:
        print("  Stream:", s)
        
    # Check for subtitles or episode objects
    episodes = []
    for i, item in enumerate(data):
        if isinstance(item, dict) and ('episodeNumber' in item or 'episodeNo' in item or 'episodes' in item or 'playUrl' in item or 'videoUrl' in item):
            resolved = devalue_deref(i, data)
            episodes.append(resolved)
    print(f"Episode-like objects found: {len(episodes)}")
    if episodes:
        print("Sample episode object:", json.dumps(episodes[0], indent=2, ensure_ascii=False)[:500])
else:
    print("No devalue script found")
