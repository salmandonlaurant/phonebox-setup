import json, urllib.request

BASE = "http://127.0.0.1:8765"
FONT_RULE = 'html,body{font-family:"SF Pro Rounded","Hiragino Maru Gothic ProN",Quicksand,Nunito,"Trebuchet MS",Roboto,system-ui,sans-serif}\n'

with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

d = cfg.setdefault("display", {})
d["theme"] = "amoled"
d["accent"] = "#0A84FF"
d["artTint"] = False
d["appearance"] = {
    "style": "cards",
    "font": "rounded",
    "radius": 22,
    "gap": 10,
    "padding": 14,
    "pagePadding": 10,
    "fontScale": 108,
}

for page in cfg.get("pages", []):
    for w in page.get("widgets", []):
        if w.get("type") != "html":
            continue
        html = w.get("options", {}).get("html", "")
        if not html or FONT_RULE.strip() in html:
            continue
        if "<style>" in html:
            html = html.replace("<style>", "<style>" + FONT_RULE, 1)
        else:
            html = "<style>" + FONT_RULE + "</style>" + html
        w["options"]["html"] = html

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=20) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)
print("theme:", d["theme"], "accent:", d["accent"], "appearance:", d["appearance"])
