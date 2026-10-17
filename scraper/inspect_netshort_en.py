import httpx
import json
import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

print("=== NETSHORT ENGLISH DRAMAS ===")
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get("https://netshort.com/")
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', r.text)
    combined = ""
    for c in chunks:
        try:
            combined += json.loads(f'"{c}"')
        except Exception:
            combined += c
            
    # Search for shortPlay objects
    matches = re.findall(r'\{"shortPlayLibraryId":[^}]*?"shortPlayName":"([^"]+)"[^}]*?"shortPlayCover":"([^"]+)"[^}]*?\}', combined)
    print("English NetShort dramas found:", len(matches))
    for name, cover in matches[:10]:
        print(f"  EN Drama: {name} | Cover: {cover[:60]}...")
