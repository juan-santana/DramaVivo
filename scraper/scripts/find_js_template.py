import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
webpack = client.get("https://dramashorts.io/_next/static/chunks/webpack-b29db2cc729feb6e.js").text

# Find how JS chunk URL is constructed
idx = webpack.find(".js")
while idx != -1:
    print(webpack[max(0, idx-60):min(len(webpack), idx+60)])
    idx = webpack.find(".js", idx+1)
    if idx > 2000:
        break
