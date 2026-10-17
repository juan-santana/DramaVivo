import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
manifest = client.get('https://dramashorts.io/_next/static/nsE5iNPLI8q36GG8kZ9eI/_buildManifest.js').text
routes = re.findall(r'"(/[a-zA-Z0-9_\-\[\]/]*)"\s*:\s*\[([^\]]+)\]', manifest)
for r, chunks in routes:
    print(f"Route: {r} -> Chunks: {chunks}")
