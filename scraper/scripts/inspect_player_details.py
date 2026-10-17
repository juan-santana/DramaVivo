import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
for chunk in ["static/chunks/2792-c5044e53344c9f73.js", "static/chunks/7675-fe2ac99e1bfba2f0.js"]:
    text = client.get(f"https://dramashorts.io/_next/{chunk}").text
    print(f"=== {chunk} (len={len(text)}) ===")
    for word in ['video', 'src', 'hls', 'm3u8', 'mp4', 'episodes', 'player', 'cdn', 'stream']:
        matches = [m.start() for m in re.finditer(word, text, re.I)]
        print(f"  {word}: {len(matches)}")
        for idx in matches[:2]:
            print("    ", text[max(0, idx-40):min(len(text), idx+80)])
