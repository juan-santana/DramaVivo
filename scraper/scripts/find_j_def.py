import httpx
import re

client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'}, follow_redirects=True)
text = client.get("https://dramashorts.io/_next/static/chunks/4171-0878cec46122d38f.js").text
# Find definitions of j
for m in re.finditer(r'([a-zA-Z0-9_\$]+\s*=\s*.*?j\s*=)', text):
    print("Match:", m.group(0)[:100])
# Or search for "function j(" or "const j=" or "let j=" or "var j="
for pattern in [r'var\s+j\s*=', r'let\s+j\s*=', r'const\s+j\s*=', r'function\s+j\s*\(', r'j\s*=\s*_\([0-9]+\)']:
    m = re.findall(pattern, text)
    if m:
        print("Found definition pattern:", pattern, m)

# Let's search where _(number) is imported in 4171
imports = re.findall(r'_\([0-9]+\)', text)
print("Webpack imports in 4171:", set(imports))
