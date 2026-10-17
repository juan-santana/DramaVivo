import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
for chunk in ["static/chunks/3300-a5510cd5c463003f.js", "static/chunks/1938-0bb56093b76dbe3e.js"]:
    text = client.get(f"https://dramashorts.io/_next/{chunk}").text
    print(f"--- {chunk} (len={len(text)}) ---")
    for pattern in [r'https?://[a-zA-Z0-9_\-\./]+', r'/\w+/\w+/\w+']:
        m = re.findall(r'https?://(?:cdn|api|stream|video)[a-zA-Z0-9_\-\./]*', text)
        if m:
            print("  CDN/API found:", set(m[:10]))
            break
    # search video player logic or HLS
    for word in ['videoUrl', 'streamUrl', 'm3u8', 'blob:', 'Hls', 'VideoPlayer', 'player', 'jwplayer', 'videojs']:
        count = len(re.findall(word, text, re.I))
        if count > 0:
            print(f"  Keyword {word}: {count}")
