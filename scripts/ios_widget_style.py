import json, urllib.request

BASE = "http://127.0.0.1:8765"

with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

# ---- 1. Global iOS-style widget appearance ----
d = cfg.setdefault("display", {})
d["appearance"] = {
    "style": "cards",
    "font": "rounded",
    "fontScale": 112,
    "radius": 28,
    "gap": 12,
    "padding": 15,
    "pagePadding": 12,
    "border": False,
    "shadow": True,
}

# ---- 2. Frosted-glass skin for the custom HTML widgets ----
GLASS = """
<style>
/* iOS-style frosted widget surface */
html,body{font-family:"SF Pro Rounded","Hiragino Maru Gothic ProN",Quicksand,Nunito,"Trebuchet MS",Roboto,system-ui,sans-serif!important}
#wrap{
  background:linear-gradient(180deg,rgba(44,44,46,.74),rgba(26,26,28,.70))!important;
  -webkit-backdrop-filter:blur(30px) saturate(190%);
  backdrop-filter:blur(30px) saturate(190%);
  border:1px solid rgba(255,255,255,.13)!important;
  border-radius:28px!important;
  box-shadow:0 12px 40px rgba(0,0,0,.5)!important;
  padding:14px!important;
}
#logo{border-radius:9px!important}
.s,.s2,.row,.card,.song{
  border-radius:18px!important;
  background:rgba(255,255,255,.075)!important;
  border:1px solid rgba(255,255,255,.085)!important;
  min-height:46px;
}
.s:active,.s2:active,.song:active{transform:scale(.97)}
#f,#q,#search{
  border-radius:20px!important;
  background:rgba(118,118,128,.24)!important;
  border:1px solid rgba(255,255,255,.09)!important;
  padding:10px 14px!important;
  font-size:14px!important;
}
#bt,.hd b{font-size:16px!important;font-weight:650!important;letter-spacing:-.02em!important}
.n,.sname,.title{font-size:13px!important;font-weight:500!important}
#ct,.sub{font-size:11px!important;font-weight:600!important;letter-spacing:.04em!important}
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.18);border-radius:5px}
</style>
"""

for page in cfg.get("pages", []):
    for w in page.get("widgets", []):
        if w.get("type") != "html":
            continue
        opts = w.setdefault("options", {})
        html = opts.get("html", "")
        if "iOS-style frosted widget surface" in html:
            continue
        # append override after existing markup/styles so it wins
        opts["html"] = html + GLASS
        # let the iframe paint its own frosted card over the wallpaper
        opts["transparent"] = True
        w["appearance"] = {"style": "borderless", "radius": 0, "padding": 0,
                           "border": False, "shadow": False}

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=20) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)
print("appearance:", d["appearance"])
