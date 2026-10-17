import httpx
client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
webpack = client.get("https://dramashorts.io/_next/static/chunks/webpack-b29db2cc729feb6e.js").text
idx = webpack.find("o.u=")
print(webpack[idx:idx+1500])
