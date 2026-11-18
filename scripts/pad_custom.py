import json, urllib.request
BASE = "http://127.0.0.1:8765"
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))
n = 0
for page in cfg.get("pages", []):
    for w in page.get("widgets", []):
        if w.get("type") == "html" and w.get("id") not in (None, "liquid-glass"):
            w["appearance"] = {"style": "borderless", "radius": 0, "padding": 14,
                               "border": False, "shadow": False}
            n += 1
body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)
print("custom panels padded:", n)
