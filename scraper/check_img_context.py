import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

html = open('shorttv_es.html', encoding='utf-8').read()
count = 0
for m in re.finditer(r'https://akamai-static\.shorttv\.live/[^\s"\'<>]+(?:\.jpg|\.png|\.webp)', html):
    start = max(0, m.start() - 200)
    end = min(len(html), m.end() + 200)
    print(f"Match #{count}:")
    print(html[start:end])
    print('='*60)
    count += 1
    if count >= 3:
        break
