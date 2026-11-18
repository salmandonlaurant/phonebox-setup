import json, urllib.request

BASE = "http://127.0.0.1:8765"
with urllib.request.urlopen(BASE + "/api/config", timeout=15) as r:
    cfg = json.loads(r.read().decode()).get("config", {})

pages = cfg.get("pages", [])
sys = next(p for p in pages if p.get("id") == "system")
print("SYSTEM_PAGE enabled:", sys.get("enabled"))
print("SYSTEM_WIDGETS:", [(w.get("id"), w.get("type"), w.get("x"), w.get("y"), w.get("w"), w.get("h")) for w in sys["widgets"]])
print("SYSTEM_OPTIONS:", [w.get("options") for w in sys["widgets"] if w.get("id") == "launchers"])

for p in pages:
    for w in p["widgets"]:
        if w.get("id") == "ytm-picker":
            h = w["options"]["html"]
            print("PICKER:", p["id"], "| songs:", h.count('"v":'), "| debounce:", "__ytBusy" in h, "| section:", "Your YouTube Music activity" in h)
            break

ytm = [s for s in cfg.get("shortcuts", []) if s.get("id", "").startswith("ytm-")]
print("YT_SHORTCUTS:", len(ytm), "| first:", ytm[0]["label"] if ytm else None, "| last:", ytm[-1]["label"] if ytm else None)
ym = next((s for s in cfg["shortcuts"] if s.get("id") == "ytmusic"), None)
print("YT_MUSIC_MAIN:", ym.get("cmd") if ym else None, "|", ym.get("args") if ym else None)

i = json.load(urllib.request.urlopen(BASE + "/api/info", timeout=15))
print("TABLET:", i.get("connected"), "via", i.get("via"))
