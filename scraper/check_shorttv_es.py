import httpx
import re
import json
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def check_shorttv_es():
    url = "https://www.shorttv.live/es"
    r = httpx.get(url, headers=headers, follow_redirects=True, timeout=20)
    print("ShortTV ES status:", r.status_code, "Length:", len(r.text))
    open('shorttv_es.html', 'w', encoding='utf-8').write(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    dramas = []
    for a in soup.find_all('a', href=True):
        if '/drama/' in a['href']:
            title = a.get_text(strip=True)
            img = a.find('img')
            img_src = img['src'] if img and img.has_attr('src') else ''
            if not title and img and img.has_attr('alt'):
                title = img['alt']
            dramas.append({'href': a['href'], 'title': title, 'img': img_src})
    print(f"Dramas in ShortTV ES: {len(dramas)}")
    for d in dramas[:5]:
        print(" ", d)

if __name__ == '__main__':
    check_shorttv_es()
