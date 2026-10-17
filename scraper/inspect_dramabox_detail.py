import httpx
import json
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

print("=== EXAMINING DRAMABOX __NEXT_DATA__ ===")
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get("https://www.dramabox.com/es")
    soup = BeautifulSoup(r.text, "html.parser")
    next_data_tag = soup.find("script", id="__NEXT_DATA__")
    if next_data_tag:
        data = json.loads(next_data_tag.string)
        page_props = data.get("props", {}).get("pageProps", {})
        big_list = page_props.get("bigList", [])
        small_data = page_props.get("smallData", [])
        print("bigList length:", len(big_list))
        if big_list:
            print("Sample bigList item keys:", list(big_list[0].keys()))
            print("Sample bigList item:", json.dumps(big_list[0], indent=2, ensure_ascii=False)[:500])
        print("\nsmallData length:", len(small_data))
        if small_data:
            print("Sample smallData item:", str(small_data[0])[:300])

print("\n=== EXAMINING DRAMABOX DRAMA DETAIL PAGE ===")
detail_url = "https://www.dramabox.com/es/drama/41000110515/Escape-With-Boss-s-Baby"
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r_detail = client.get(detail_url)
    print("Detail status:", r_detail.status_code)
    soup_detail = BeautifulSoup(r_detail.text, "html.parser")
    next_tag = soup_detail.find("script", id="__NEXT_DATA__")
    if next_tag:
        d = json.loads(next_tag.string)
        props = d.get("props", {}).get("pageProps", {})
        print("Detail pageProps keys:", list(props.keys()))
        for k in props.keys():
            val = props[k]
            if isinstance(val, dict):
                print(f"  {k} keys:", list(val.keys()))
            elif isinstance(val, list):
                print(f"  {k} list len:", len(val))
                if val:
                    print(f"    sample {k}[0]:", str(val[0])[:200])
            else:
                print(f"  {k}:", str(val)[:100])
