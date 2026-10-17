import re
import json
import sys

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

def inspect_file(filename, is_es=True):
    print(f"=== Inspecting {filename} ===")
    html = open(filename, encoding='utf-8').read()
    match = re.search(r'<script[^>]*>(\[\["ShallowReactive".*?\])</script>', html, re.DOTALL)
    if not match:
        print("No script payload found")
        return []
    data = json.loads(match.group(1))
    
    unique = {}
    for i, item in enumerate(data):
        if isinstance(item, dict) and ('title' in item or 'dramaTitle' in item or 'name' in item):
            resolved = devalue_deref(i, data)
            if isinstance(resolved, dict):
                title = resolved.get('title') or resolved.get('dramaTitle') or resolved.get('name')
                cover = resolved.get('imageUrl') or resolved.get('cover') or resolved.get('coverUrl') or resolved.get('poster')
                drama_id = resolved.get('dramaId') or resolved.get('id')
                if title and isinstance(title, str) and (cover or drama_id):
                    # Filter out episode-level objects or menu items
                    if len(title) > 2 and not title.startswith('Episode'):
                        key = str(drama_id) if drama_id else title
                        if key not in unique:
                            unique[key] = {
                                'dramaId': drama_id,
                                'title': title,
                                'cover': cover,
                                'desc': resolved.get('description') or resolved.get('desc') or resolved.get('intro') or '',
                                'keys': list(resolved.keys())
                            }
    print(f"Found {len(unique)} unique dramas in {filename}")
    for k, v in list(unique.items())[:5]:
        print(f"  - [{v['dramaId']}] {v['title']} (Cover: {str(v['cover'])[:40]}...)")
        print(f"    Keys: {v['keys']}")
    return list(unique.values())

if __name__ == '__main__':
    inspect_file('shorttv_es.html', is_es=True)
    inspect_file('shorttv_home.html', is_es=False)
