import json, urllib.request

BASE = "http://127.0.0.1:8765"
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

LAUNCHERS = [
    {
        "id": "launcher-epic", "label": "Epic",
        "icon": "🎮", "color": "#E4E4E4", "toggle": False,
        "cmd": r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe",
    },
    {
        "id": "launcher-steam", "label": "Steam",
        "icon": "🕹️", "color": "#1B2838", "toggle": False,
        "cmd": r"C:\Program Files (x86)\Steam\steam.exe",
    },
    {
        "id": "launcher-battlenet", "label": "Battle.net",
        "icon": "⚔️", "color": "#00AEFF", "toggle": False,
        "cmd": r"C:\Program Files (x86)\Battle.net\Battle.net.exe",
    },
]

sc = cfg.setdefault("shortcuts", [])
existing = {s.get("id") for s in sc}
for item in LAUNCHERS:
    if item["id"] in existing:
        # keep it up to date if the path ever changes
        s = next(s for s in sc if s.get("id") == item["id"])
        s.update(item)
    else:
        sc.append(item)

# System page: make room for a 3-button launcher row at bottom right.
sys_page = next(p for p in cfg["pages"] if p["id"] == "system")
widgets = sys_page["widgets"]
for w in widgets:
    if w.get("id") == "meters":
        w.update({"x": 0, "y": 3, "w": 4, "h": 3})
    elif w.get("id") == "chart-3":
        w.update({"x": 4, "y": 3, "w": 4, "h": 3})

widgets[:] = [w for w in widgets if w.get("id") != "launchers"]
widgets.append({
    "id": "launchers", "type": "shortcuts",
    "x": 8, "y": 3, "w": 4, "h": 3,
    "options": {
        "ids": [i["id"] for i in LAUNCHERS],
        "columns": 3,
    },
    "appearance": {"style": "cards", "radius": 20, "padding": 12},
})

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)
print("system widgets:", [(w["id"], w["x"], w["y"], w["w"], w["h"]) for w in widgets])
