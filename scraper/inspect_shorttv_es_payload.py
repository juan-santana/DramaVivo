import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

def devalue_deref(idx, data, seen=None):
    if seen is None:
        seen = set()
    if not isinstance(idx, int) or idx < 0 or idx >= len(data):
        return idx
    if idx in seen:
        return f"<circular {idx}>"
    seen.add(idx)
    
    val = data[idx]
    if isinstance(val, (str, bool, float)) or val is None:
        return val
    if isinstance(val, int):
        return devalue_deref(val, data, seen)
    if isinstance(val, list):
        if len(val) == 2 and isinstance(val[0], str) and isinstance(val[1], int):
            return devalue_deref(val[1], data, seen)
        return [devalue_deref(item, data, seen.copy()) for item in val]
    if isinstance(val, dict):
        res = {}
        for k, v in val.items():
            res[k] = devalue_deref(v, data, seen.copy())
        return res
    return val

def test_shorttv_es():
    html = open('shorttv_es.html', encoding='utf-8').read()
    match = re.search(r'<script[^>]*>(\[\["ShallowReactive".*?\])</script>', html, re.DOTALL)
    if not match:
        print("No script payload")
        return
    data = json.loads(match.group(1))
    print(f"ShortTV ES payload length: {len(data)}")
    
    # Look for items with imageUrl or title
    for i, item in enumerate(data):
        if isinstance(item, dict) and 'title' in item and 'imageUrl' in item:
            resolved = devalue_deref(i, data)
            print("Found drama card:", json.dumps(resolved, indent=2, ensure_ascii=False))
            break

if __name__ == '__main__':
    test_shorttv_es()
