import httpx

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://dramashorts.io/'}, follow_redirects=True)

test_urls = [
    "https://cdn.dramashorts.io/video/7FavIbRxN4DLjAJTrzlusdPb/trailer/manifest.m3u8",
    "https://cdn.dramashorts.io/video/7FavIbRxN4DLjAJTrzlusdPb/1/manifest.m3u8",
    "https://cdn.dramashorts.io/video/7FavIbRxN4DLjAJTrzlusdPb/n9zYZ7caG8GPPDI25N_cvCu3/manifest.m3u8",
    "https://cdn.dramashorts.io/video/7FavIbRxN4DLjAJTrzlusdPb/b4c093b6-350f-4d5a-8133-b3a9fb983fff/manifest.m3u8",
]

for url in test_urls:
    try:
        r = client.get(url)
        print(f"URL: {url} -> Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200:
            print("  First 3 lines of m3u8:")
            for line in r.text.splitlines()[:4]:
                print("   ", line)
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")
