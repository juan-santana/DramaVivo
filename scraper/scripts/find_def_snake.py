import httpx
client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
text = client.get("https://dramashorts.io/_next/static/chunks/pages/_app-f54aaaa714c69418.js").text

idx = text.find('convertKeysToSnakeCase=')
if idx == -1:
    idx = text.find('convertKeysToSnakeCase')
print(text[idx:idx+400])
