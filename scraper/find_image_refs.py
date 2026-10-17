import re
import json
import sys
from inspect_shorttv_cards import devalue_deref

sys.stdout.reconfigure(encoding='utf-8')

html = open('shorttv_es.html', encoding='utf-8').read()
match = re.search(r'<script[^>]*>(\[\["ShallowReactive".*?\])</script>', html, re.DOTALL)
data = json.loads(match.group(1))

# Find any objects with 'akamai-static.shorttv.live'
matches = []
for i, item in enumerate(data):
    if isinstance(item, str) and 'akamai-static.shorttv.live' in item:
        # Check who references this index
        referrers = []
        for j, other in enumerate(data):
            if isinstance(other, dict) and any(v == i for v in other.values()):
                referrers.append((j, other))
            elif isinstance(other, list) and i in other:
                referrers.append((j, other))
        matches.append((i, item, referrers))

print(f"Total image strings found: {len(matches)}")
for idx, img_url, refs in matches[:10]:
    print(f"\nImage idx {idx}: {img_url}")
    for ref_idx, ref_obj in refs:
        print(f"  Referenced by #{ref_idx}: {ref_obj}")
        resolved = devalue_deref(ref_idx, data)
        print(f"  Resolved #{ref_idx}:", json.dumps(resolved, ensure_ascii=False)[:300])
