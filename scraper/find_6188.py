import httpx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with httpx.Client(timeout=15) as client:
    soup_resp = client.get("https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(soup_resp.text, "html.parser")
    for s in soup.find_all("script"):
        src = s.get("src")
        if src and "/_next/" in src:
            chunk = client.get(f"https://netshort.com{src}")
            if "6188:" in chunk.text:
                print("Found module 6188 in:", src)
                idx = chunk.text.find("6188:")
                print("Definition of 6188:", chunk.text[idx:idx+600])
                break
