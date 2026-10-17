import httpx
import sys

sys.stdout.reconfigure(encoding='utf-8')

# NetShort playVoucher test
netshort_stream = "https://cfcdn.netshort.com/ooTnIAA2Tog6UdGNC4rLi9f5Ae16qPILKgef7e?a=0&auth_key=1792616963-132c0adb320945c691c9a306950711ad-0-aaa057c36a1858b73bfc6be06c939d08&br=793&bt=793&cd=0%7C0%7C0&ch=0&cr=0&cs=0&cv=1&dr=3&ds=3&eid=f1ea6475bc2b4c28b24218bfb37aaa3e&er=0&l=2026100806093217108887F18B9B8525DE&lr=&mime_type=video_mp4&net=0&pl=0&qs=0&rc=M2tuNHk5cmt4ZDozMzZoNEApNmQ6ZWU0N2U1NzVlOjloaWctYV9pMm"

# GoodShort m3u8 test
goodshort_stream = "https://v3.goodshort.com/mts/books/972/31001113972/551781/dixnbbmikv/origin1/yv1abvaagv.m3u8?expiredTime=1793427819&tul=1b445ed9a01e297aff65c73a02914c023c87aeb2d2fec590780b1ff8167a223cd92ffb5eda2d8191402ca5ebd909ebd673156f711fcf5bcf9137a0c25338ff09"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Origin": "http://localhost:5173",
    "Referer": "https://www.goodshort.com/",
}

with httpx.Client(headers=headers, follow_redirects=True, timeout=10) as client:
    print("Testing NetShort MP4...")
    r1 = client.head(netshort_stream)
    print("NetShort HEAD status:", r1.status_code, "Content-Type:", r1.headers.get("content-type"), "CORS:", r1.headers.get("access-control-allow-origin"))
    
    print("\nTesting GoodShort M3U8...")
    r2 = client.get(goodshort_stream)
    print("GoodShort GET status:", r2.status_code, "Content-Type:", r2.headers.get("content-type"), "CORS:", r2.headers.get("access-control-allow-origin"))
    print("GoodShort m3u8 snippet:", r2.text[:300])
