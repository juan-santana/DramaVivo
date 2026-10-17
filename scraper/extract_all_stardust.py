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

def extract_all():
    html = open('stardusttv_home.html', encoding='utf-8').read()
    match = re.search(r'<script[^>]*>(\[\["ShallowReactive".*?\])</script>', html, re.DOTALL)
    data = json.loads(match.group(1))
    
    series_found = []
    
    # Traverse through all items looking for dicts with 'id', 'english_name' or 'name', 'cover_path'
    for i, item in enumerate(data):
        if isinstance(item, dict) and 'cover_path' in item and ('english_name' in item or 'name' in item):
            resolved = devalue_deref(i, data)
            name = resolved.get('english_name') or resolved.get('name')
            intro = resolved.get('intro') or ''
            cover = resolved.get('cover_path') or resolved.get('cover_snapshot_path') or ''
            filepath = resolved.get('filepath') or ''
            sid = resolved.get('id')
            tag = resolved.get('ornaments_auto_tag_name') or 'Español'
            
            if name and cover and isinstance(name, str) and isinstance(cover, str) and cover.startswith('http'):
                series_found.append({
                    'id': f"stardust-{sid}",
                    'raw_id': sid,
                    'title': name,
                    'synopsis': intro,
                    'poster': cover,
                    'filepath': filepath,
                    'tag': tag
                })
                
    # Deduplicate by raw_id or title
    unique_series = {}
    for s in series_found:
        if s['raw_id'] not in unique_series:
            unique_series[s['raw_id']] = s
            
    print(f"Extracted {len(unique_series)} unique StardustTV series!")
    for s in list(unique_series.values())[:10]:
        print(f"- [{s['id']}] {s['title']} | Cover: {s['poster'][:50]}... | Stream: {s['filepath'][:50]}...")
        
    return list(unique_series.values())

if __name__ == '__main__':
    extract_all()
