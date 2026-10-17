import httpx
import json
import re
from bs4 import BeautifulSoup

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, follow_redirects=True)
r = client.get('https://dramashorts.io/es')
soup = BeautifulSoup(r.text, 'html.parser')
data = json.loads(soup.find('script', id='__NEXT_DATA__').string)
discover = data['props']['pageProps']['discover']

all_movies = {}
for block in discover:
    block_type = block.get('type')
    block_data = block.get('data', {})
    block_title = block_data.get('title') or block_type
    movies = block_data.get('movies', [])
    print(f"Block '{block_title}': {len(movies)} movies")
    for m in movies:
        mid = m['id']
        if mid not in all_movies:
            all_movies[mid] = {
                'id': mid,
                'title': m.get('title'),
                'slug': m.get('slug'),
                'description': m.get('description'),
                'cover': m.get('images', {}).get('cover'),
                'coverWithTitle': m.get('images', {}).get('coverWithTitle'),
                'episodesCount': m.get('episodesCount'),
                'genre': m.get('genre', {}).get('title') if m.get('genre') else 'Drama',
                'viewsCount': m.get('viewsCount'),
                'block': block_title
            }

print(f"\nTotal unique series discovered: {len(all_movies)}")
for i, (mid, m) in enumerate(list(all_movies.items())[:12]):
    print(f"{i+1}. {m['title']} | Género: {m['genre']} | {m['episodesCount']} eps | Views: {m['viewsCount']}")
