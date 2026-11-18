import json
import re
import urllib.request

BASE = "http://127.0.0.1:8765"

for u in ["/api/refresh?reload=true", "/api/goto/home?countdown=0"]:
    req = urllib.request.Request(BASE + u, data=b"", method="POST")
    print(u, urllib.request.urlopen(req, timeout=15).status)

c = json.load(open(r"C:\Users\Admin\AppData\Roaming\PhoneBox\config.json", encoding="utf-8"))
ids = {s["id"] for s in c["shortcuts"]}
home = [p for p in c["pages"] if p["id"] == "home"][0]
w = [x for x in home["widgets"] if x["id"] == "media-cat"][0]
html_text = w["options"]["html"]
used = set(re.findall(r'data-run="([^"]+)"', html_text))
print("widget shortcuts used:", sorted(used))
print("missing:", sorted(used - ids))
print("has volume slider:", 'type="range"' in html_text or "volr" in html_text)
print("cat dance animation present:", "@keyframes hop" in html_text)
info = json.load(urllib.request.urlopen(BASE + "/api/info", timeout=10))
print("connected:", info["connected"], info["via"])
