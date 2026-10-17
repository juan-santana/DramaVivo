import httpx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with httpx.Client(timeout=15) as client:
    c1 = client.get("https://netshort.com/_next/static/chunks/2519-8205e9faaabd75ea.js").text
    idx = c1.find("/web/v4/short_play")
    print("Snippet in 2519:", c1[max(0, idx-100):min(len(c1), idx+300)])
    
    c2 = client.get("https://netshort.com/_next/static/chunks/6600-938d05f4f11e6e45.js").text
    idx2 = c2.find("baseUrl")
    print("Snippet in 6600:", c2[max(0, idx2-50):min(len(c2), idx2+200)])
