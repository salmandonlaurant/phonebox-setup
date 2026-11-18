import json, urllib.request

BASE = "http://127.0.0.1:8765"
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

REPL = [
    ("#bt{font-size:14px", "#bt{font-size:16px"),
    ("#ct{font-size:10px", "#ct{font-size:11px"),
    ("#f{width:100%;box-sizing:border-box;padding:8px 12px", "#f{width:100%;box-sizing:border-box;padding:10px 14px"),
    ("border-radius:20px;border:1px solid var(--line);background:var(--card);color:var(--txt);font-size:12px",
     "border-radius:20px;border:1px solid var(--line);background:var(--card);color:var(--txt);font-size:14px"),
    ("#sect{font-size:10px", "#sect{font-size:11px"),
    ("cursor:pointer;transition:background .18s,border-color .18s,transform .12s}",
     "cursor:pointer;transition:background .18s,border-color .18s,transform .12s;padding:8px 10px}"),
    (".th{width:46px;height:46px", ".th{width:52px;height:52px"),
    (".ph{width:46px;height:46px", ".ph{width:52px;height:52px"),
    (".tt{font-size:12px", ".tt{font-size:14px"),
    (".st{font-size:10px", ".st{font-size:12px"),
    (".pl{width:20px;flex:0 0 auto;text-align:center;color:var(--sub);font-size:13px}",
     ".pl{width:24px;flex:0 0 auto;text-align:center;color:var(--sub);font-size:15px}"),
    (".none{color:var(--sub);font-size:12px", ".none{color:var(--sub);font-size:13px"),
]

changed = 0
for p in cfg["pages"]:
    for w in p["widgets"]:
        if w.get("id") != "ytm-picker":
            continue
        h = w["options"]["html"]
        for old, new in REPL:
            if old in h:
                h = h.replace(old, new)
                changed += 1
        w["options"]["html"] = h
print("REPLACEMENTS:", changed)

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh?reload=true", data=b"", method="POST"), timeout=20) as r:
    print("reload:", r.status)
