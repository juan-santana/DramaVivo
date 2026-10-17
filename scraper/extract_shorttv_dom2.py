import re
import json
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

def extract_shorttv_catalog():
    for f, lang in [('shorttv_es.html', 'Español'), ('shorttv_home.html', 'English')]:
        print(f"\n=== Processing {f} ({lang}) ===")
        html = open(f, encoding='utf-8').read()
        soup = BeautifulSoup(html, 'html.parser')
        
        # In ShortTV, each card has an <a> with card-image and an <a> with title
        # Or look for container divs / cards
        cards = soup.find_all('div', class_=re.compile(r'card|drama-item|item'))
        print(f"Total card divs found: {len(cards)}")
        
        # Alternatively find all <a> with href to drama
        dramas = {}
        for a in soup.find_all('a', href=re.compile(r'/(?:es/)?drama/[a-zA-Z0-9\-_]+')):
            href = a['href']
            # Find closest parent container or siblings for image & title
            parent = a.parent
            for _ in range(3):
                if parent and (parent.find('img') or parent.find('h2') or parent.find('h3')):
                    break
                if parent:
                    parent = parent.parent
            
            img = parent.find('img') if parent else None
            poster = None
            if img:
                poster = img.get('data-src') or img.get('src')
                if not poster and img.get('srcset'):
                    poster = img.get('srcset').split(' ')[0]
            
            title = a.get_text(strip=True)
            if not title and img:
                title = img.get('alt')
            if not title and parent:
                title_el = parent.find(re.compile(r'h\d|title|name'))
                if title_el:
                    title = title_el.get_text(strip=True)
            
            # Clean title
            if title and len(title) > 2 and not title.startswith('Episode'):
                # Extract clean slug/id
                slug = href.split('/')[-1]
                if slug not in dramas:
                    dramas[slug] = {
                        'id': f"shorttv-{slug}",
                        'slug': slug,
                        'title': title,
                        'poster': poster,
                        'source_url': f"https://www.shorttv.live{href}",
                        'language': lang
                    }
        print(f"Extracted {len(dramas)} valid {lang} dramas!")
        for d in list(dramas.values())[:8]:
            print(f"  [{d['id']}] {d['title']}")
            print(f"    Poster: {d['poster']}")
            print(f"    URL: {d['source_url']}")
            
if __name__ == '__main__':
    extract_shorttv_catalog()
