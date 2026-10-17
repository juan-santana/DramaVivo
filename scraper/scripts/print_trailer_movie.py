import httpx
import json
from bs4 import BeautifulSoup

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, follow_redirects=True)
r = client.get("https://dramashorts.io/es/trailer/f5d26df3-3893-4447-8460-9b73a9892b10")
soup = BeautifulSoup(r.text, 'html.parser')
data = json.loads(soup.find('script', id='__NEXT_DATA__').string)
movie = data['props']['pageProps']['movieDetails']['movie']
print(json.dumps(movie, indent=2))
