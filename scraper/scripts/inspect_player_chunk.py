import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
chunk_url = "https://dramashorts.io/_next/static/chunks/pages/shorts/[movieId]/[episode]-320cf632517677e3.js"
res = client.get(chunk_url)
print("Chunk length:", len(res.text))

# Search for video, hls, m3u8, player, or cdn in chunk
terms = ['m3u8', 'video', 'stream', 'cdn', 'player', 'manifest', 'src', 'url']
for t in ['m3u8', 'videoUrl', 'streamUrl', 'playUrl', 'videoSrc', 'hlsUrl', 'cdn']:
    matches = [m.start() for m in re.finditer(t, res.text, re.IGNORECASE)]
    print(f"Matches for '{t}':", len(matches))
    for idx in matches[:5]:
        start = max(0, idx - 80)
        end = min(len(res.text), idx + 120)
        print(f"  Snippet around {t}: ...{res.text[start:end]}...")
