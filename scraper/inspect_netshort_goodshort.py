import httpx
import json
import re
from bs4 import BeautifulSoup
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

print("=== INSPECTING NETSHORT ===")
try:
    with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
        r = client.get("https://netshort.com/")
        soup = BeautifulSoup(r.text, "html.parser")
        print("NetShort title:", soup.title.string if soup.title else "No title")
        # Check __NEXT_DATA__ or any JSON embedded in script tags
        for s in soup.find_all("script"):
            if s.get("id") == "__NEXT_DATA__":
                print("Found __NEXT_DATA__!")
            text = s.string or ""
            if "props" in text or "dramas" in text or "series" in text or "window.__INITIAL_STATE__" in text:
                print("Interesting script match (len %d):" % len(text), text[:300])
        
        # Check any links on the page
        links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
        print("Total links found on NetShort:", len(links))
        drama_links = [l for l in links if any(k in l for k in ["/drama", "/series", "/watch", "/detail", "/play", "/es", "/en"])]
        print("Sample drama/navigation links:", drama_links[:10])
        
        # Check if sitemap exists
        sm_resp = client.get("https://netshort.com/sitemap.xml")
        print("Sitemap status:", sm_resp.status_code, "Length:", len(sm_resp.text))
        if sm_resp.status_code == 200:
            print("Sitemap snippet:", sm_resp.text[:500])
            
except Exception as e:
    print("NetShort error:", e)

print("\n=== INSPECTING GOODSHORT ===")
try:
    with httpx.Client(headers=headers, follow_redirects=True, timeout=15) as client:
        r = client.get("https://www.goodshort.com/")
        soup = BeautifulSoup(r.text, "html.parser")
        print("GoodShort title:", soup.title.string if soup.title else "No title")
        
        # Look for links
        links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
        print("Total links found on GoodShort:", len(links))
        drama_links = [l for l in links if any(k in l for k in ["/drama", "/detail", "/book", "/video", "/play", "/film"])]
        print("Sample drama links:", drama_links[:10])
        
        # Look for sitemap
        sm_resp = client.get("https://www.goodshort.com/sitemap.xml")
        print("GoodShort sitemap status:", sm_resp.status_code, "Length:", len(sm_resp.text))
        if sm_resp.status_code == 200:
            print("Sitemap snippet:", sm_resp.text[:500])
            
        # Check robots.txt
        rb = client.get("https://www.goodshort.com/robots.txt")
        print("Robots.txt status:", rb.status_code, "\n", rb.text[:400])

except Exception as e:
    print("GoodShort error:", e)
