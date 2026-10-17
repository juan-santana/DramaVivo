import httpx
import json
import re
import sys
from bs4 import BeautifulSoup
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

test_urls = [
    "https://netshort.com/episode/the-ex-husbands-regret-2110939611852431361",
    "https://netshort.com/es/episode/la-sirvienta-reclam%C3%B3-su-corona-2110547948523937794"
]

with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    for url in test_urls:
        r = client.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        title_tag = soup.find("title").text if soup.find("title") else ""
        og_title = soup.find("meta", property="og:title")
        og_desc = soup.find("meta", property="og:description")
        og_img = soup.find("meta", property="og:image")
        
        # playVoucher
        vouchers = re.findall(r'playVoucher\\*":\\*"([^"\\]+)', r.text)
        subs = re.findall(r'subtitleList\\*":(\[[^\]]+\])', r.text)
        
        print("\nURL:", url.split("/")[-1])
        print("Title Tag:", title_tag)
        print("OG Title:", og_title["content"] if og_title else "N/A")
        print("OG Desc:", (og_desc["content"][:100] if og_desc else "N/A"))
        print("OG Img:", (og_img["content"][:80] if og_img else "N/A"))
        print("Vouchers:", len(vouchers))
        print("Subs:", len(subs))
