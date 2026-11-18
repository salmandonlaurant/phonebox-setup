import json, urllib.request

BASE = "http://127.0.0.1:8765"
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

page = next(p for p in cfg["pages"] if p["id"] == "system")
ids = ["launcher-epic", "launcher-steam", "launcher-battlenet"]

# Keep only the glass backing and one full-page launcher grid.
page["widgets"] = [{
    "id": "launchers", "type": "shortcuts",
    "x": 0, "y": 0, "w": 12, "h": 6,
    "options": {"ids": ids, "columns": 3},
    "appearance": {"style": "cards", "radius": 28, "padding": 16},
}]

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
print("widgets:", [(w["id"], w["type"], w["w"], w["h"]) for w in page["widgets"]])
