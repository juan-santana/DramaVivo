import httpx
import re
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://dramashorts.io/es',
}

client = httpx.Client(headers=headers, follow_redirects=True, timeout=15)
r = client.get('https://dramashorts.io/es/shorts/f5d26df3-3893-4447-8460-9b73a9892b10')
soup = BeautifulSoup(r.text, 'html.parser')
scripts = [s['src'] for s in soup.find_all('script', src=True)]

for s in scripts:
    url = f"https://dramashorts.io{s}" if s.startswith('/') else s
    res = client.get(url)
    
    # search for api base or environment variables
    env_matches = re.findall(r'NEXT_PUBLIC_[A-Z0-9_]+', res.text)
    if env_matches:
        print(f"Env in {s}:", set(env_matches))
        
    # search for endpoints with episodes or stream
    for pattern in [r'/api/[a-zA-Z0-9_\-/]+', r'https?://api\.[a-zA-Z0-9\.-]+/[a-zA-Z0-9_\-/]+', r'https?://[a-zA-Z0-9\.-]+/[a-zA-Z0-9_\-/]*\.(?:m3u8|mp4)']:
        m = re.findall(pattern, res.text)
        if m:
            print(f"Match pattern {pattern} in {s}:", set(m[:10]))
