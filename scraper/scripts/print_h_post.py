import httpx
client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
text = client.get("https://dramashorts.io/_next/static/chunks/pages/_app-f54aaaa714c69418.js").text

idx = text.find('https://web-api.dramashorts.io/v1')
print("h.post implementation:")
print(text[idx:idx+600])
