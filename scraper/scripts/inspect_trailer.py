import httpx
import json
from bs4 import BeautifulSoup

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, follow_redirects=True)
r = client.get("https://dramashorts.io/es/trailer/f5d26df3-3893-4447-8460-9b73a9892b10")
print("Trailer status:", r.status_code)
soup = BeautifulSoup(r.text, 'html.parser')
next_data = soup.find('script', id='__NEXT_DATA__')
if next_data:
    data = json.loads(next_data.string)
    props = data.get('props', {}).get('pageProps', {})
    print("Trailer pageProps keys:", list(props.keys()))
    for k in props:
        if k not in ['messages', 'locale']:
            print(f"{k}:", json.dumps(props[k], indent=2)[:400])
