import json, urllib.request

BASE = "http://127.0.0.1:8765"
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

first = next((s for s in cfg["shortcuts"] if s.get("id", "").startswith("ytm-")), None)
if not first:
    print("no ytm shortcut found")
    raise SystemExit
vid = first["args"].split('"')[-2]
print("first video:", vid)

for s in cfg["shortcuts"]:
    if s.get("id") == "ytmusic":
        s["cmd"] = r"C:\Windows\System32\wscript.exe"
        s["args"] = f'//B "C:\\Users\\Admin\\AppData\\Local\\PhoneBox\\ytm-run.vbs" "{vid}"'
        print("ytmusic redirected")

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh?reload=true", data=b"", method="POST"), timeout=20) as r:
    print("reload:", r.status)
