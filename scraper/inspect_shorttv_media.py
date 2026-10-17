import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def find_media():
    for f in ['shorttv_es.html', 'shorttv_home.html']:
        print(f"=== File: {f} ===")
        html = open(f, encoding='utf-8').read()
        imgs = re.findall(r'https?://[^\s"\'<>]+(?:\.jpg|\.png|\.webp|\.jpeg)', html)
        print(f"Found {len(imgs)} image matches:")
        for img in list(set(imgs))[:10]:
            print(f"  {img}")
            
        vids = re.findall(r'https?://[^\s"\'<>]+(?:\.m3u8|\.mp4)', html)
        print(f"Found {len(vids)} video matches:")
        for vid in list(set(vids))[:10]:
            print(f"  {vid}")
            
        # Also check for links /drama/ or /es/drama/
        dramas = re.findall(r'(?:https://www\.shorttv\.live)?/(?:es/)?drama/[a-zA-Z0-9\-_]+', html)
        print(f"Found {len(dramas)} drama link matches:")
        for d in list(set(dramas))[:10]:
            print(f"  {d}")

if __name__ == '__main__':
    find_media()
