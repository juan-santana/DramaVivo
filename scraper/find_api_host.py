import httpx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Search for the API baseUrl in chunk 1255 or 1356 or main-app
with httpx.Client(timeout=15) as client:
    resp = client.get("https://netshort.com/_next/static/chunks/app/%5Blocale%5D/episode/%5Bepisode%5D/page-1c1217f311686ba2.js")
    # Search for baseURL or apiUrl or https://
    urls = re.findall(r'https?://[a-zA-Z0-9.-]+\.netshort\.com', resp.text)
    print("Domains in page.js:", set(urls))
    
    # Check layout chunk
    resp2 = client.get("https://netshort.com/_next/static/chunks/1255-8befde0980f5cba9.js")
    urls2 = re.findall(r'https?://[a-zA-Z0-9.-]+\.netshort\.com', resp2.text)
    print("Domains in 1255:", set(urls2))
    
    resp3 = client.get("https://netshort.com/_next/static/chunks/1356-497180fb2a2b715f.js")
    urls3 = re.findall(r'https?://[a-zA-Z0-9.-]+\.netshort\.com', resp3.text)
    print("Domains in 1356:", set(urls3))
    
    # Search for "/web/v4" across all scripts
    soup_resp = client.get("https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(soup_resp.text, "html.parser")
    for s in soup.find_all("script"):
        src = s.get("src")
        if src and "/_next/" in src:
            chunk = client.get(f"https://netshort.com{src}")
            if "api" in chunk.text.lower() and ("https://" in chunk.text):
                api_hosts = re.findall(r'https://(?:api|gateway|server|h5|m)[a-zA-Z0-9.-]*\.netshort\.com', chunk.text)
                if api_hosts:
                    print("Found API host in", src[-25:], ":", set(api_hosts))
