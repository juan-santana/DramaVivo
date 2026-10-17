import httpx
client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
text = client.get("https://dramashorts.io/_next/static/chunks/411.9ed8b2d8f035af5b.js").text

idx = text.find("videoSrc")
while idx != -1:
    print("--- videoSrc context ---")
    print(text[max(0, idx-200):min(len(text), idx+200)])
    idx = text.find("videoSrc", idx+1)
