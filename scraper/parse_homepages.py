import sys
import re
import json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

def parse_shorttv():
    html = open('shorttv_home.html', encoding='utf-8').read()
    print("=== SHORTTV PARSER ===")
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check all scripts for JSON data
    for i, s in enumerate(soup.find_all('script')):
        content = s.string or ""
        if len(content) > 1000:
            print(f"Script #{i} length: {len(content)}")
            # check for keywords
            if 'data' in content or 'props' in content or 'dramas' in content:
                print(f"  Snippet: {content[:300].strip()}...")

def parse_stardusttv():
    html = open('stardusttv_home.html', encoding='utf-8').read()
    print("\n=== STARDUSTTV PARSER ===")
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check all scripts for JSON data
    for i, s in enumerate(soup.find_all('script')):
        content = s.string or ""
        if len(content) > 1000:
            print(f"Script #{i} length: {len(content)}")
            if 'episode' in content or 'title' in content or 'video' in content or 'url' in content:
                print(f"  Snippet: {content[:300].strip()}...")

if __name__ == '__main__':
    parse_shorttv()
    parse_stardusttv()
