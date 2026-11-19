"""Add a Pair Phone button to the PhoneBox dashboard.

Tapping it runs a hidden helper on the PC that generates a fresh QR pairing
code and opens it in the PC's browser, ready to scan with the phone.
"""
import json
import urllib.request

BASE = "http://127.0.0.1:8765"
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

shortcuts = cfg.setdefault("shortcuts", [])
by_id = {s["id"]: s for s in shortcuts}
pair = {
    "id": "pair-phone",
    "label": "Pair Phone (QR)",
    "icon": "📱",
    "color": "#22c55e",
    "cmd": "C:\\Windows\\System32\\wscript.exe",
    "args": '//B "C:\\Users\\Admin\\AppData\\Local\\PhoneBox\\pair-phone-run.vbs"',
    "toggle": False,
}
if "pair-phone" in by_id:
    by_id["pair-phone"].update(pair)
else:
    shortcuts.append(pair)

# Add it as a fourth big launcher on the "system" page.
syspage = [p for p in cfg["pages"] if p["id"] == "system"][0]
launchers = [w for w in syspage["widgets"] if w.get("id") == "launchers"][0]
ids = launchers.setdefault("options", {}).setdefault("ids", [])
if "pair-phone" not in ids:
    ids.append("pair-phone")

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
print("system launchers:", ids)
print("pair shortcut:", json.dumps(pair, ensure_ascii=False))
