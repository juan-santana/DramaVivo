import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
manifest = client.get('https://dramashorts.io/_next/static/nsE5iNPLI8q36GG8kZ9eI/_buildManifest.js').text
# Extract all chunk paths
chunks = set(re.findall(r'static/chunks/[a-zA-Z0-9_\-\.]+\.js', manifest))
# Also add app and main
chunks.update(["static/chunks/pages/_app-f54aaaa714c69418.js", "static/chunks/main-163e93eae70e6470.js", "static/chunks/411.9ed8b2d8f035af5b.js"])

for c in chunks:
    try:
        t = client.get(f"https://dramashorts.io/_next/{c}").text
        if 'loadEpisodeAccess' in t:
            print(f"Found loadEpisodeAccess in {c}!")
            idx = t.find('loadEpisodeAccess')
            print(t[max(0, idx-100):min(len(t), idx+400)])
    except Exception as e:
        pass
