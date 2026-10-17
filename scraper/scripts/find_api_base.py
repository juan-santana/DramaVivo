import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
text = client.get("https://dramashorts.io/_next/static/chunks/pages/_app-f54aaaa714c69418.js").text

idx = text.find('web-episode-access')
print("Context around web-episode-access:")
print(text[max(0, idx-400):min(len(text), idx+100)])

# Find where h is defined
for m in re.finditer(r'baseURL\s*:\s*[\'"][^\'"]+[\'"]', text):
    print("Base URL found:", m.group(0))

# Also search for api.dramashorts or backend URL
for m in re.finditer(r'https?://[a-zA-Z0-9_\-\.]*(?:api|backend|gateway)[a-zA-Z0-9_\-\.]*', text):
    print("API domain found:", m.group(0))
