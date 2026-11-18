import json, os, shutil, urllib.request

BASE = "http://127.0.0.1:8765"
SYNC_DIR = r"C:\Users\Admin\AppData\Local\PhoneBox\wallpaper-sync"
SRC = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Themes\TranscodedWallpaper")
DST = os.path.join(SYNC_DIR, "wallpaper.jpg")

os.makedirs(SYNC_DIR, exist_ok=True)
shutil.copy2(SRC, DST)
print("copied wallpaper:", os.path.getsize(DST), "bytes")

with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

cfg.setdefault("photos", {})["folder"] = SYNC_DIR
cfg["photos"]["subfolders"] = False

bg = {
    "id": "pc-wallpaper",
    "type": "photos",
    "x": 0, "y": 0, "w": 12, "h": 6,
    "options": {"fit": "cover", "interval": 3600, "shuffle": False},
    "appearance": {"style": "borderless", "radius": 0, "padding": 0, "border": False, "shadow": False},
}

for page in cfg.get("pages", []):
    widgets = page.setdefault("widgets", [])
    widgets[:] = [w for w in widgets if w.get("id") != "pc-wallpaper"]
    widgets.insert(0, json.loads(json.dumps(bg)))

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=20) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)

with urllib.request.urlopen(BASE + "/api/photos", timeout=15) as r:
    print("photos api:", r.read().decode("utf-8")[:300])
