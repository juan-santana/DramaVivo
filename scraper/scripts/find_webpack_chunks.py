import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
webpack = client.get("https://dramashorts.io/_next/static/chunks/webpack-b29db2cc729feb6e.js").text

# In webpack runtime, chunk mapping is like {805: "...", 888: "..."}
matches = re.findall(r'(\d+):"([a-f0-9]+)"', webpack)
chunk_map = {m[0]: m[1] for m in matches}
for cid in ['805', '888', '7675', '2792', '411']:
    if cid in chunk_map:
        print(f"Chunk {cid} -> static/chunks/{cid}-{chunk_map[cid]}.js")
    else:
        # check if it's named without hash
        print(f"Chunk {cid} not in direct map")

# Let's search for 805 or 7675 in webpack text
for cid in ['805', '888', '7675', '2792']:
    idx = webpack.find(cid)
    if idx != -1:
        print(f"Around {cid}:", webpack[max(0, idx-40):min(len(webpack), idx+60)])
