import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
text = client.get("https://dramashorts.io/_next/static/chunks/411.9ed8b2d8f035af5b.js").text

idx = text.find(",y]")
if idx == -1:
    idx = text.find(",y)")
print("Context around y declaration:")
print(text[max(0, idx-200):min(len(text), idx+300)])
