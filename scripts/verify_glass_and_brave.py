import json, urllib.request, subprocess

BASE = "http://127.0.0.1:8765"
c = json.load(open(r"C:\Users\Admin\AppData\Roaming\PhoneBox\config.json", encoding="utf-8"))
p = [x for x in c["pages"] if x["id"] == "system"][0]
g = [w for w in p["widgets"] if w.get("id") == "liquid-glass"][0]
html = g["options"]["html"]
print("SYSTEM_GLASS_PANELS:", html.count('class="g"'))
print("SYSTEM_GLASS_HTML_LEN:", len(html))

out = subprocess.run(["powershell", "-NoProfile", "-Command",
    "(Get-Process brave -ErrorAction SilentlyContinue | Measure-Object).Count"],
    capture_output=True, text=True, timeout=30)
print("BRAVE_PROCESSES:", out.stdout.strip())

info = json.load(urllib.request.urlopen(BASE + "/api/info", timeout=15))
print("CONNECTED:", info.get("connected"), info.get("via"))
