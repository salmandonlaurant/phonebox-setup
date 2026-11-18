import json, urllib.request

BASE = "http://127.0.0.1:8765"
CLIENT_ID = "1572354807363149834"
CLIENT_SECRET = "D0DE0BGyPSjjRvLyduTHBXmBjyo3uUsW"

with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

cfg["discord"] = {
    "enabled": True,
    "clientId": CLIENT_ID,
    "clientSecret": CLIENT_SECRET,
}

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=20) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)
