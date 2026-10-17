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

# Test 1: web-episode-list
r1 = client.post("https://web-api.dramashorts.io/v1/web-episode-list", json={"movie_id": "f5d26df3-3893-4447-8460-9b73a9892b10"})
print("Test 1 web-episode-list status:", r1.status_code)
if r1.status_code == 200:
    print("Sample episode list:", json.dumps(r1.json()[:2], indent=2))
else:
    print(r1.text)

# Test 2: web-episode-access with only movie_id and episode_id
r2 = client.post("https://web-api.dramashorts.io/v1/web-episode-access", json={
    "movie_id": "f5d26df3-3893-4447-8460-9b73a9892b10",
    "episode_id": "b4c093b6-350f-4d5a-8133-b3a9fb983fff"
})
print("\nTest 2 web-episode-access status:", r2.status_code)
print(r2.text)
