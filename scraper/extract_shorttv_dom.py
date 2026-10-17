import re
import json
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

def extract_shorttv_catalog():
    # 1. From shorttv_es.html (Spanish)
    html_es = open('shorttv_es.html', encoding='utf-8').read()
    soup_es = BeautifulSoup(html_es, 'html.parser')
    
    # Check all <a> links
    es_links = soup_es.find_all('a', href=re.compile(r'/es/drama/'))
    print(f"Total /es/drama/ <a> links: {len(es_links)}")
    
    es_dramas = {}
    for a in es_links:
        href = a['href']
        img = a.find('img')
        poster = img.get('src') if img else None
        title = a.get_text(strip=True)
        if not title and img:
            title = img.get('alt') or ''
        
        # Clean title
        if title:
            drama_id = href.split('/')[-1]
            if drama_id not in es_dramas:
                es_dramas[drama_id] = {
                    'id': f"shorttv-{drama_id}",
                    'slug': drama_id,
                    'title': title,
                    'poster': poster,
                    'source_url': f"https://www.shorttv.live{href}",
                    'language': 'Español'
                }
    
    print(f"Extracted {len(es_dramas)} unique Spanish dramas from HTML tags:")
    for d in list(es_dramas.values())[:5]:
        print(f"  [{d['id']}] {d['title']} | Cover: {d['poster']} | URL: {d['source_url']}")
        
    # 2. From shorttv_home.html (English)
    html_en = open('shorttv_home.html', encoding='utf-8').read()
    soup_en = BeautifulSoup(html_en, 'html.parser')
    
    en_links = soup_en.find_all('a', href=re.compile(r'/drama/'))
    print(f"Total /drama/ <a> links: {len(en_links)}")
    en_dramas = {}
    for a in en_links:
        href = a['href']
        if '/es/drama/' in href:
            continue
        img = a.find('img')
        poster = img.get('src') if img else None
        title = a.get_text(strip=True)
        if not title and img:
            title = img.get('alt') or ''
        if title:
            drama_id = href.split('/')[-1]
            if drama_id not in en_dramas:
                en_dramas[drama_id] = {
                    'id': f"shorttv-{drama_id}",
                    'slug': drama_id,
                    'title': title,
                    'poster': poster,
                    'source_url': f"https://www.shorttv.live{href}",
                    'language': 'English'
                }
    print(f"Extracted {len(en_dramas)} unique English dramas from HTML tags:")
    for d in list(en_dramas.values())[:5]:
        print(f"  [{d['id']}] {d['title']} | Cover: {d['poster']} | URL: {d['source_url']}")

if __name__ == '__main__':
    extract_shorttv_catalog()
