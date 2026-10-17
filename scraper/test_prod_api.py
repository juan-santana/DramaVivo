import httpx
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=utf-8",
    "Origin": "https://netshort.com",
    "Referer": "https://netshort.com/es/episode/mi-esposo-me-crey%C3%B3-ciega-2104831753981931521",
    "OS": "4",
    "canary": "v1",
    "version": "1.2.0",
}

with httpx.Client(headers=headers, timeout=15) as client:
    payload = {
        "shortPlayId": "2104831753981931521",
        "episodeNo": 2
    }
    r = client.post("https://netshort.com/prod-web-api/web/v4/short_play/episode_info", json=payload)
    print("Status:", r.status_code)
    print("Headers:", dict(r.headers))
    print("Body:", r.text[:600])
