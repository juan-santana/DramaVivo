import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
manifest = client.get('https://dramashorts.io/_next/static/nsE5iNPLI8q36GG8kZ9eI/_buildManifest.js').text
match = re.search(r'function\(([a-z,]+)\)\{return\{.*?s=.*?;', manifest)
print(manifest[:300])
# Let's search where s, c, u are defined
lines = manifest.split(';')
for l in lines[:10]:
    print(l)
