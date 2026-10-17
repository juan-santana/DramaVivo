import sys
import re
import json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

def analyze_nuxt(filename, label):
    html = open(filename, encoding='utf-8').read()
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script')
    payload_script = None
    for s in scripts:
        if s.string and len(s.string) > 10000:
            payload_script = s.string
            break
            
    print(f"\n==================== {label} ====================")
    if not payload_script:
        print("No large payload script found")
        return
        
    # Let's search for URLs, titles, and IDs in payload
    # Find all image URLs
    img_urls = re.findall(r'https?://[^\s",\'\]\}]+\.(?:jpg|jpeg|png|webp)', payload_script)
    print(f"Image URLs ({len(img_urls)}):")
    for u in img_urls[:5]:
        print(" ", u)
        
    # Find video URLs
    video_urls = re.findall(r'https?://[^\s",\'\]\}]+\.(?:mp4|m3u8)', payload_script)
    print(f"Video URLs ({len(video_urls)}):")
    for v in video_urls[:5]:
        print(" ", v)
        
    # In Nuxt 3, the payload is a flat array where numbers are references to other indices.
    # Let's see if we can parse the top-level array:
    try:
        data = json.loads(payload_script)
        print(f"Top-level is JSON array of {len(data)} elements!")
        # Let's inspect some strings or dictionaries in the array
        sample_objects = [x for x in data if isinstance(x, dict) and any(k in x for k in ['title', 'name', 'dramaName', 'cover', 'poster', 'episodes', 'dramaId', 'bookId'])]
        print(f"Found {len(sample_objects)} candidate drama/episode dicts!")
        for obj in sample_objects[:10]:
            print("  Obj:", obj)
            
        # Also check strings with 'http' or titles
        string_elements = [x for x in data if isinstance(x, str) and len(x) > 3]
        print(f"Total string elements: {len(string_elements)}")
        # Print sample interesting strings
        dramas = [s for s in string_elements if any(w in s.lower() for w in ['billionaire', 'ceo', 'venganza', 'prometid', 'amor', 'esposo', 'matrimonio', 'reina', 'mafia', 'revenge'])]
        print(f"Drama-like title strings ({len(dramas)}):", dramas[:10])
    except Exception as e:
        print("JSON parse error:", e)

if __name__ == '__main__':
    analyze_nuxt('shorttv_home.html', 'SHORTTV')
    analyze_nuxt('stardusttv_home.html', 'STARDUSTTV')
