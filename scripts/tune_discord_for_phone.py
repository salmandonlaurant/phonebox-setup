import json, urllib.request

BASE = "http://127.0.0.1:8765"
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

work = [p for p in cfg["pages"] if p["id"] == "work"][0]

# Rebalance the split: the soundboard was squeezed into 4 columns (~260 CSS px
# on the A32), so give it 5 and let the control widget keep a comfortable 7.
for w in work["widgets"]:
    if w.get("id") == "discord-control":
        w.update({"x": 0, "y": 0, "w": 7, "h": 6})
    elif w.get("id") == "discord-sfx":
        w.update({"x": 7, "y": 0, "w": 5, "h": 6})

        h = w["options"]["html"]
        old_style_end = h.index("</style>") + len("</style>")
        new_style = """<style>
html,body{margin:0;height:100%;font-family:"SF Pro Rounded","Hiragino Maru Gothic ProN",Quicksand,Nunito,"Trebuchet MS",Roboto,system-ui,sans-serif;background:transparent;overflow:hidden}
:root{--ac:#5865f2;--txt:#ececf2;--sub:#9a9aa6;--card:rgba(255,255,255,.06);--line:rgba(255,255,255,.10)}
#wrap{display:flex;flex-direction:column;height:100%;box-sizing:border-box;gap:10px}
#hd{flex:0 0 auto}
#brand{display:flex;align-items:center;gap:9px;margin-bottom:9px}
#logo{width:28px;height:28px;border-radius:50%;background:var(--ac);display:flex;align-items:center;justify-content:center;font-size:15px;color:#fff}
#bt{font-size:17px;font-weight:700;letter-spacing:-.01em;color:var(--txt)}
#ct{font-size:12px;color:var(--sub);margin-left:auto}
#f{width:100%;box-sizing:border-box;padding:11px 15px;border-radius:22px;border:1px solid var(--line);background:var(--card);color:var(--txt);font-size:15px;outline:none}
#f::placeholder{color:var(--sub)}
#f:focus{border-color:rgba(88,101,242,.8);background:rgba(255,255,255,.09)}
#list{flex:1 1 auto;overflow-y:auto;-webkit-overflow-scrolling:touch;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;padding:2px 2px 10px;align-content:start}
.s{display:flex;align-items:center;gap:8px;min-width:0;min-height:48px;box-sizing:border-box;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--txt);padding:9px 8px;cursor:pointer;text-align:left;transition:background .18s,border-color .18s,transform .12s}
.s:hover{background:rgba(88,101,242,.16)}
.s:active,.s.hit{background:rgba(88,101,242,.32);border-color:rgba(88,101,242,.7);transform:scale(.97)}
.e{font-size:18px;flex:0 0 auto;width:26px;text-align:center}
.n{font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.none{grid-column:1/-1;color:var(--sub);font-size:14px;text-align:center;padding:16px}
</style>"""
        w["options"]["html"] = new_style + h[old_style_end:]

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
print("widgets:", [(w["id"], w["x"], w["y"], w["w"], w["h"]) for w in work["widgets"]])
