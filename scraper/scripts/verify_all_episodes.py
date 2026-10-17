import httpx
import json
import re
from bs4 import BeautifulSoup

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://dramashorts.io/'}, follow_redirects=True)
r = client.get('https://dramashorts.io/es/shorts/f5d26df3-3893-4447-8460-9b73a9892b10')
soup = BeautifulSoup(r.text, 'html.parser')
data = json.loads(soup.find('script', id='__NEXT_DATA__').string)
episodes = data['props']['pageProps']['episodes']

print(f"Total episodes in series: {len(episodes)}")

# Check first 5 episodes and episode 10, 20, 50
sample_indices = [0, 1, 2, 3, 4, 9, 19, 49]
for idx in sample_indices:
    if idx < len(episodes):
        ep = episodes[idx]['episode']
        cover = ep['coverUrl']
        # Extract movie hash and episode hash from coverUrl
        # https://cdn.dramashorts.io/img/episodes-previews/<movie_hash>/<ep_hash>/cover.jpeg
        m = re.search(r'episodes-previews/([^/]+)/([^/]+)/', cover)
        if m:
            movie_hash, ep_hash = m.groups()
            video_url = f"https://cdn.dramashorts.io/video/{movie_hash}/{ep_hash}/manifest.m3u8"
            res = client.get(video_url)
            print(f"Episode {ep['index']} ({ep['title']}): video status={res.status_code}, len={len(res.text)}")
            print(f"   Video URL: {video_url}")
            print(f"   Thumbnail: {cover}")
        else:
            print(f"Episode {ep['index']}: could not extract hashes from {cover}")
