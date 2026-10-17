import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
text = client.get("https://dramashorts.io/_next/static/chunks/pages/player/[movieId]-af4fef1063780840.js").text
print("Player chunk len:", len(text))
for word in ['video', 'stream', 'hls', 'm3u8', 'mp4', 'src', 'url', 'token', 'play']:
    matches = [m.start() for m in re.finditer(word, text, re.I)]
    print(f"Keyword {word}: {len(matches)}")
    for idx in matches[:3]:
        print("  Snippet:", text[max(0, idx-50):min(len(text), idx+100)])
