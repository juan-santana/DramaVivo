import httpx
client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
text = client.get("https://dramashorts.io/_next/static/chunks/4171-0878cec46122d38f.js").text
idx = text.find("let j=")
print(text[idx:idx+300])
