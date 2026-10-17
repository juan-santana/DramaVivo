import httpx
import sys

sys.stdout.reconfigure(encoding='utf-8')

with httpx.Client(timeout=15) as client:
    chunk = client.get("https://netshort.com/_next/static/chunks/8000-bf7f7efcf55919f3.js").text
    idx = chunk.find("97539:")
    print("Module 97539 code snippet:")
    print(chunk[idx:idx+2500])
