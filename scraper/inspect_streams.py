import httpx
import json
import re
from bs4 import BeautifulSoup
import sys
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

print("=== INSPECTING NETSHORT EPISODE PAGE ===")
netshort_url = "https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521"
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get(netshort_url)
    print("NetShort episode status:", r.status_code)
    
    # Check for m3u8, mp4, video tags, or json chunks
    video_links = re.findall(r'https?://[^\s"\'<>]+\.(?:m3u8|mp4)[^\s"\'<>]*', r.text)
    print("Direct video urls found:", len(video_links))
    for v in set(video_links):
        print("  Video URL:", v[:120])
        
    vtt_links = re.findall(r'https?://[^\s"\'<>]+\.(?:vtt|srt)[^\s"\'<>]*', r.text)
    print("VTT/SRT subtitles found:", len(vtt_links))
    for s in set(vtt_links):
        print("  Subtitle URL:", s[:120])
        
    # Check chunks for episode data
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', r.text)
    full_str = "".join(chunks)
    # Search for video / playUrl / streamUrl / cdn
    matches = re.findall(r'(?:videoUrl|playUrl|streamUrl|m3u8|url)["\']?\s*:\s*["\'](https?://[^"\']+)["\']', full_str)
    print("URL matches in next_f:", len(matches))
    for m in matches[:5]:
        print("  Stream match:", m[:120])

    # Check cover / poster
    posters = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp)[^\s"\'<>]*', r.text)
    print("Sample posters:", list(set(posters))[:5])

print("\n=== INSPECTING GOODSHORT DRAMA PAGE ===")
goodshort_url = "https://www.goodshort.com/drama/blood-and-bones-of-the-disowned-daughter-31001113972"
with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
    r = client.get(goodshort_url)
    print("GoodShort drama status:", r.status_code)
    
    video_links = re.findall(r'https?://[^\s"\'<>]+\.(?:m3u8|mp4)[^\s"\'<>]*', r.text)
    print("GoodShort video urls found:", len(video_links))
    for v in set(video_links):
        print("  Video URL:", v[:120])
        
    soup = BeautifulSoup(r.text, "html.parser")
    # Check for script tags with json data
    for s in soup.find_all("script"):
        text = s.string or ""
        if "playlet" in text or "video" in text or "chapter" in text or "episode" in text:
            print("Found script with drama data, len:", len(text), text[:300])
            
    # Check if there is an API called by the page or if GoodShort uses an API
    # Let's inspect scripts to find API baseUrl
    for s in soup.find_all("script"):
        src = s.get("src", "")
        if "app." in src or "vendor." in src:
            js_resp = client.get(src)
            api_matches = re.findall(r'https?://api[^\s"\'<>]+', js_resp.text)
            print("APIs in", src[-20:], ":", set(api_matches[:5]))
            endpoints = re.findall(r'["\'](/api/[^"\']+|/web/[^"\']+|/drama/[^"\']+)["\']', js_resp.text)
            print("Endpoints in", src[-20:], ":", set(endpoints[:10]))
