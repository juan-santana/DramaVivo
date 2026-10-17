import urllib.request

url = "https://www.reelshort.com/_next/static/chunks/pages/_app-e3704c0c6d458909.js"
headers = {"User-Agent": "Mozilla/5.0"}
js = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=10).read().decode("utf-8")

idx = js.find("55598:")
print(js[idx:idx+800])
