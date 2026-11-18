import json, re, urllib.request

BASE = "http://127.0.0.1:8765"
VBS = r"C:\Users\Admin\AppData\Local\PhoneBox\ytm-run.vbs"
SONGS_FILE = r"C:\Users\Admin\AppData\Local\Temp\phonebox-account-songs.json"

songs = json.load(open(SONGS_FILE, encoding="utf-8"))
assert songs and all(re.fullmatch(r"[A-Za-z0-9_-]{11}", s["id"]) for s in songs)

with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

# 1) Replace all ytm-* shortcuts with the account-derived list.
kept = [s for s in cfg["shortcuts"] if not s.get("id", "").startswith("ytm-")]
for i, song in enumerate(songs, 1):
    kept.append({
        "id": f"ytm-{i:02d}",
        "label": song["title"][:90],
        "icon": "♪",
        "color": "#FF0033",
        "cmd": r"C:\Windows\System32\wscript.exe",
        "args": f'//B "{VBS}" "{song["id"]}"',
        "toggle": False,
    })
cfg["shortcuts"] = kept

# 2) Point the main "ytmusic" shortcut at the new first song too.
for s in cfg["shortcuts"]:
    if s.get("id") == "ytmusic":
        s["args"] = f'//B "{VBS}" "{songs[0]["id"]}"'

# 3) Rebuild the picker's song array in place (keeps styling + debounce).
picker_songs = [
    {"i": f"ytm-{i:02d}", "v": song["id"], "t": song["title"]}
    for i, song in enumerate(songs, 1)
]
new_array = "var S=" + json.dumps(picker_songs, ensure_ascii=False, separators=(",", ":")) + ";"
changed = 0
for p in cfg["pages"]:
    for w in p["widgets"]:
        if w.get("id") != "ytm-picker":
            continue
        html = w["options"].get("html", "")
        html, n = re.subn(r"var S=\[.*?\];", lambda m: new_array, html, count=1, flags=re.S)
        html = html.replace('<div id="sect">Home mix</div>',
                            '<div id="sect">Your YouTube Music activity</div>')
        w["options"]["html"] = html
        changed += n
print("PICKERS_UPDATED:", changed)

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh?reload=true", data=b"", method="POST"), timeout=20) as r:
    print("reload:", r.status)

print("YT_SHORTCUTS:", sum(1 for s in cfg["shortcuts"] if s.get("id", "").startswith("ytm-")))
print("FIRST:", songs[0]["id"], "|", songs[0]["title"])
print("TOTAL:", len(songs))
