import httpx
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Origin': 'https://dramashorts.io',
    'Referer': 'https://dramashorts.io/es/shorts/f5d26df3-3893-4447-8460-9b73a9892b10/1',
    'Content-Type': 'application/json',
    'X-Interface-Language': 'es',
    'X-OS': 'web',
    'X-OS-Version': '1.0.0',
    'X-App-Version': '1.0.0',
}

client = httpx.Client(headers=headers, timeout=15)
payload = {
    "movie_id": "f5d26df3-3893-4447-8460-9b73a9892b10",
    "episode_id": "b4c093b6-350f-4d5a-8133-b3a9fb983fff",
    "paywall_hash": None,
    "version_hash": None
}

try:
    r = client.post("https://web-api.dramashorts.io/v1/web-episode-access", json=payload)
    print("Status:", r.status_code)
    print("Response headers:", dict(r.headers))
    print("Response body:")
    print(json.dumps(r.json(), indent=2))
except Exception as e:
    print("Error:", e)
