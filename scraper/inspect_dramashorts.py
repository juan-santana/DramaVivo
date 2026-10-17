import urllib.request
import re
import json

url = "https://dramashorts.io/es/shorts/07e1642f-d17a-41c7-88e5-08bcf0fdc586"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8")

match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
if match:
    data = json.loads(match.group(1))
    page_props = data.get("props", {}).get("pageProps", {})
    print("Keys in pageProps:", list(page_props.keys()))
    print("Page props content snippet:", str(page_props)[:300])
