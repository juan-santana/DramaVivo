import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
text = client.get("https://dramashorts.io/_next/static/chunks/pages/_app-f54aaaa714c69418.js").text

for term in ['firebase', 'apiKey', 'projectId', 'authDomain', 'signInAnonymously']:
    matches = [m.start() for m in re.finditer(term, text, re.I)]
    print(f"Term '{term}': {len(matches)}")
    for idx in matches[:2]:
        print("  Snippet:", text[max(0, idx-50):min(len(text), idx+100)])
