import json, urllib.request

BASE = "http://127.0.0.1:8765"
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

for page in cfg.get("pages", []):
    if page.get("id") == "work":
        page["title"] = "Discord"
        page["widgets"] = [
            {
                "id": "discord-control",
                "type": "discord",
                "x": 0, "y": 0, "w": 6, "h": 6,
                "options": {
                    "channels": True,
                    "notifications": True,
                    "control": True,
                },
            },
            {"id": "sessions", "type": "sessions", "x": 6, "y": 0, "w": 6, "h": 3},
            {"id": "github", "type": "github", "x": 6, "y": 3, "w": 6, "h": 3},
        ]
        break
else:
    raise SystemExit("page id 'work' not found")

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=20) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)

p = [x for x in cfg["pages"] if x["id"] == "work"][0]
print("page:", p["title"], [(w["id"], w["type"], w["x"], w["y"], w["w"], w["h"]) for w in p["widgets"]])
