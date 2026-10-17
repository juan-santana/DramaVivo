import httpx
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

print("=== CHECKING NETSHORT EPISODES STRUCTURE ===")
netshort_url = "https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521"
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get(netshort_url)
    
    # Check if there is an episode list in the chunks
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', r.text)
    combined = ""
    for c in chunks:
        try:
            combined += json.loads(f'"{c}"')
        except Exception:
            combined += c
            
    # Search for all episodeId or playVoucher
    episodes = re.findall(r'\{[^{}]*?"episodeNo":\s*(\d+)[^{}]*?"playVoucher":\s*"([^"]+)"[^{}]*?\}', combined)
    print("Direct episodes with playVoucher found:", len(episodes))
    for ep_no, voucher in episodes[:5]:
        print(f"  Ep {ep_no}: {voucher[:80]}...")
        
    # Check all episode numbers listed in the drama
    all_ep_matches = re.findall(r'\{[^{}]*?"episodeId":\s*"(\d+)"[^{}]*?"episodeNo":\s*(\d+)[^{}]*?\}', combined)
    print("Total episode objects found:", len(all_ep_matches))
    if all_ep_matches:
        print("  Sample ep objects:", all_ep_matches[:5])
        
    # Also check if NetShort has an API for episode details or playback
    # Let's search for api paths in chunks
    api_paths = re.findall(r'["\'](/api/[^"\']+|https?://[^"\']+/api/[^"\']+)["\']', combined)
    print("APIs in NetShort:", set(api_paths))

print("\n=== CHECKING GOODSHORT EPISODES & SPANISH CATALOG ===")
# Let's inspect GoodShort Spanish catalog: https://www.goodshort.com/es
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get("https://www.goodshort.com/es")
    m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', r.text)
    if m:
        state = json.loads(m.group(1))
        home_module = state.get("HomeModule", {})
        book_list = home_module.get("bookList", [])
        print("GoodShort ES HomeModule bookList count:", len(book_list))
        for item in book_list[:5]:
            title = item.get("bookName") or item.get("title")
            print("  ES Drama:", title, item.get("bookResourceUrl"), "Cover:", item.get("cover"))
            
    # Also check the English drama chapters in detail
    r_en = client.get("https://www.goodshort.com/drama/blood-and-bones-of-the-disowned-daughter-31001113972")
    m_en = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', r_en.text)
    if m_en:
        state_en = json.loads(m_en.group(1))
        chapters = state_en.get("BookInfoModule", {}).get("chapterVoList", [])
        print("GoodShort Blood and Bones chapters:", len(chapters))
        for ch in chapters[:5]:
            print(f"  Ch {ch.get('index') + 1}: m3u8 = {ch.get('m3u8Path', '')[:80]}...")
