import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
manifest = client.get('https://dramashorts.io/_next/static/nsE5iNPLI8q36GG8kZ9eI/_buildManifest.js').text
for line in manifest.split(','):
    if 'shorts/[movieId]' in line:
        print(line)
