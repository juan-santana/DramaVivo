import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
for path in ["static/chunks/411.9ed8b2d8f035af5b.js", "static/chunks/98e2d21d.2ed255fb33044f0c.js"]:
    r = client.get(f"https://dramashorts.io/_next/{path}")
    print(f"=== {path} (status={r.status_code}, len={len(r.text)}) ===")
    if r.status_code == 200:
        for word in ['video', 'm3u8', 'mp4', 'hls', 'stream', 'cdn.', 'src', 'episode']:
            matches = [m.start() for m in re.finditer(word, r.text, re.I)]
            print(f"  {word}: {len(matches)}")
            for idx in matches[:2]:
                print("    ", r.text[max(0, idx-40):min(len(r.text), idx+80)])
