import httpx
from bs4 import BeautifulSoup
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def inspect_shorttv_detail():
    url = "https://www.shorttv.live/drama/the-muggle-kingpin-15738"
    r = httpx.get(url, headers=headers, follow_redirects=True, timeout=15)
    print("=== SHORTTV DETAIL ===")
    print("Status:", r.status_code)
    
    # Check for video tags or JSON data
    video_matches = re.findall(r'https?://[^\s"\']+\.(?:m3u8|mp4)[^\s"\']*', r.text)
    print("Video matches:", len(video_matches), video_matches[:5])
    
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('h1')
    print("Title:", title.get_text() if title else "No h1")
    
    # Check for images / posters
    imgs = [img['src'] for img in soup.find_all('img', src=True)]
    print("Images:", len(imgs), imgs[:5])
    
    # Check scripts for JSON state
    scripts = soup.find_all('script')
    for s in scripts:
        if s.string and ('episode' in s.string.lower() or 'video' in s.string.lower() or 'cover' in s.string.lower()):
            print("Script containing video/episode/cover found, length:", len(s.string))
            sample = s.string[:300].replace('\n', ' ')
            print("Sample:", sample)

def inspect_stardusttv_detail():
    url = "https://www.stardusttv.net/es/episodes/01-todo-lo-que-tomaste-ir%C3%A1-a-por-ello-22471"
    r = httpx.get(url, headers=headers, follow_redirects=True, timeout=15)
    print("\n=== STARDUSTTV DETAIL ===")
    print("Status:", r.status_code)
    
    video_matches = re.findall(r'https?://[^\s"\']+\.(?:m3u8|mp4)[^\s"\']*', r.text)
    print("Video matches:", len(video_matches), video_matches[:5])
    
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('h1')
    print("Title:", title.get_text() if title else "No h1")
    
    scripts = soup.find_all('script')
    for s in scripts:
        if s.string and ('episode' in s.string.lower() or 'video' in s.string.lower() or 'm3u8' in s.string.lower()):
            print("Script containing video/episode found, length:", len(s.string))
            sample = s.string[:300].replace('\n', ' ')
            print("Sample:", sample)

if __name__ == '__main__':
    inspect_shorttv_detail()
    inspect_stardusttv_detail()
