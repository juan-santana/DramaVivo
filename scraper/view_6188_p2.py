import httpx
import sys

sys.stdout.reconfigure(encoding='utf-8')

with httpx.Client(timeout=15) as client:
    chunk = client.get("https://netshort.com/_next/static/chunks/8000-bf7f7efcf55919f3.js").text
    idx = chunk.find("6188:")
    print("Next 3000 chars of 6188:")
    print(chunk[idx+3000:idx+6500])
