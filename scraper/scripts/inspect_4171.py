import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
text = client.get("https://dramashorts.io/_next/static/chunks/4171-0878cec46122d38f.js").text
print("4171 chunk len:", len(text))
for word in ['m3u8', 'mp4', 'hls', 'video', 'stream', 'cdn.', 'manifest']:
    matches = [m.start() for m in re.finditer(word, text, re.I)]
    print(f"Keyword {word}: {len(matches)}")
    for idx in matches[:4]:
        print("  Snippet:", text[max(0, idx-60):min(len(text), idx+100)])
