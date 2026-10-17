import httpx
client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
text = client.get("https://dramashorts.io/_next/static/chunks/411.9ed8b2d8f035af5b.js").text

idx = text.find("loadEpisodeAccess")
print("Context after loadEpisodeAccess:")
print(text[idx:idx+800])
