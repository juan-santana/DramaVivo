import httpx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

series_urls = [
    "https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521",
    "https://netshort.com/es/episode/para-sobrevivir-debo-amarla-2103784897671143426",
    "https://netshort.com/es/episode/una-mam%C3%A1-de-acero-2102973763304947713",
    "https://netshort.com/episode/the-shadow-prince-s-only-cure-2109197469616582658",
]

with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    for url in series_urls:
        r = client.get(url)
        print(f"\nChecking: {url.split('/')[-1][:40]}")
        vouchers = re.findall(r'playVoucher\\*":\\*"([^"\\]+)', r.text)
        print("  playVoucher found:", len(vouchers))
        for v in vouchers:
            clean_url = v.replace(r"\u0026", "&")
            print("  Voucher URL:", clean_url[:100])
        # Check subtitles
        subs = re.findall(r'subtitleList\\*":(\[[^\]]+\])', r.text)
        if subs:
            print("  Subtitles:", subs[0][:150].replace(r"\"", '"'))
        # Check title & synopsis
        title = re.search(r'shortPlayName\\*":\\*"([^"\\]+)', r.text)
        synopsis = re.search(r'shotIntroduce\\*":\\*"([^"\\]+)', r.text)
        cover = re.search(r'shortPlayCover\\*":\\*"([^"\\]+)', r.text)
        print(f"  Title: {title.group(1) if title else 'N/A'}")
        print(f"  Cover: {cover.group(1)[:60] if cover else 'N/A'}")
        print(f"  Synopsis: {synopsis.group(1)[:80] if synopsis else 'N/A'}...")
