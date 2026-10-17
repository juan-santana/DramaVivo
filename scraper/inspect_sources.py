import httpx
import re
import json
from bs4 import BeautifulSoup

def inspect_shorttv():
    url = "https://www.shorttv.live/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    r = httpx.get(url, headers=headers, follow_redirects=True, timeout=20)
    print("=== SHORTTV ===")
    print("Final URL:", r.url)
    print("HTML Length:", len(r.text))
    
    # Check for __NEXT_DATA__
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.DOTALL)
    if match:
        data = json.loads(match.group(1))
        print("Found __NEXT_DATA__! Keys:", list(data.keys()))
        if 'props' in data:
            print("Props keys:", list(data['props'].keys()))
            page_props = data['props'].get('pageProps', {})
            print("pageProps keys:", list(page_props.keys()))
            for k in page_props:
                val = page_props[k]
                if isinstance(val, list):
                    print(f"  {k}: list of {len(val)} items")
                elif isinstance(val, dict):
                    print(f"  {k}: dict with keys {list(val.keys())[:5]}")
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a', href=True)
        drama_links = [a['href'] for a in links if '/drama' in a['href'] or '/watch' in a['href'] or '/video' in a['href'] or '/detail' in a['href']]
        print("Found drama links:", len(drama_links), drama_links[:10])

def inspect_stardusttv():
    url = "https://www.stardusttv.net/es"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    r = httpx.get(url, headers=headers, follow_redirects=True, timeout=20)
    print("\n=== STARDUSTTV ===")
    print("Final URL:", r.url)
    print("HTML Length:", len(r.text))
    
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.DOTALL)
    if match:
        data = json.loads(match.group(1))
        print("Found __NEXT_DATA__! Keys:", list(data.keys()))
        if 'props' in data:
            print("Props keys:", list(data['props'].keys()))
            page_props = data['props'].get('pageProps', {})
            print("pageProps keys:", list(page_props.keys()))
            for k in page_props:
                val = page_props[k]
                if isinstance(val, list):
                    print(f"  {k}: list of {len(val)} items")
                elif isinstance(val, dict):
                    print(f"  {k}: dict with keys {list(val.keys())[:5]}")
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a', href=True)
        drama_links = [a['href'] for a in links if '/drama' in a['href'] or '/watch' in a['href'] or '/video' in a['href'] or '/detail' in a['href']]
        print("Found drama links:", len(drama_links), drama_links[:10])

if __name__ == "__main__":
    inspect_shorttv()
    inspect_stardusttv()
