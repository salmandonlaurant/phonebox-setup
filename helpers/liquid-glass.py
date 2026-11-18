import base64, io, json, os, urllib.request
from PIL import Image, ImageFilter

BASE = "http://127.0.0.1:8765"

# ---- build a heavily blurred copy of the current PC wallpaper ----
src = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Themes\TranscodedWallpaper")
im = Image.open(src).convert("RGB")
W = 960
H = round(im.height * W / im.width)
im = im.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(22))
buf = io.BytesIO()
im.save(buf, "JPEG", quality=62, optimize=True)
BLUR = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
print("blurred wallpaper:", W, "x", H, "base64 chars:", len(BLUR))

CSS = """<style>
html,body{margin:0;height:100%;background:transparent;overflow:hidden;pointer-events:none}
#g{display:grid;width:100%;height:100%;box-sizing:border-box;
   grid-template-columns:repeat(12,minmax(0,1fr));
   grid-template-rows:repeat(6,minmax(0,1fr));
   gap:12px}
.g{position:relative;border-radius:30px;overflow:hidden;
   background-repeat:no-repeat;
   box-shadow:inset 0 1px 1px rgba(255,255,255,.42),
              inset 0 0 0 1px rgba(255,255,255,.12),
              inset 0 -1px 1px rgba(0,0,0,.22),
              0 12px 34px rgba(0,0,0,.45)}
.g::before{content:"";position:absolute;inset:0;border-radius:inherit;
   background:linear-gradient(135deg,rgba(255,255,255,.20),rgba(255,255,255,.045) 46%,rgba(255,255,255,.12));
   pointer-events:none}
.g::after{content:"";position:absolute;left:12%;right:12%;top:1px;height:1px;
   background:linear-gradient(90deg,transparent,rgba(255,255,255,.65),transparent);
   pointer-events:none}
</style>
"""

def pct(v, total):
    return round(v * 100.0 / total, 3)

with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

for page in cfg.get("pages", []):
    page["widgets"] = [w for w in page.get("widgets", []) if w.get("id") != "liquid-glass"]

panels = 0
for page in cfg.get("pages", []):
    divs = []
    for w in page.get("widgets", []):
        if w.get("id") in ("pc-wallpaper", "liquid-glass"):
            continue
        x, y = int(w.get("x", 0)), int(w.get("y", 0))
        ww, hh = int(w.get("w", 1)), int(w.get("h", 1))
        # Crop the full-page blurred wallpaper to this widget's slice of the 12x6 grid.
        sx = 12.0 / ww * 100 if ww else 100
        sy = 6.0 / hh * 100 if hh else 100
        px = pct(x, 12 - ww) if ww < 12 else 0
        py = pct(y, 6 - hh) if hh < 6 else 0
        style = (f"grid-area:{y+1}/{x+1}/span {hh}/span {ww};"
                 f"background-image:url('{BLUR}');"
                 f"background-size:{sx:.3f}% {sy:.3f}%;"
                 f"background-position:{px:.3f}% {py:.3f}%")
        divs.append(f'<div class="g" style="{style}"></div>')
        panels += 1
    if not divs:
        continue
    html = CSS + '<div id="g">' + "".join(divs) + "</div>"
    overlay = {
        "id": "liquid-glass",
        "type": "html",
        "x": 0, "y": 0, "w": 12, "h": 6,
        "options": {"html": html, "transparent": True},
        "appearance": {"style": "borderless", "radius": 0, "padding": 0,
                       "border": False, "shadow": False},
    }
    page["widgets"].insert(1, overlay)

# The custom panels now sit on the global glass, so drop their own milky gradient.
MARK = '<style>\n/* iOS-style frosted widget surface */'
removed = 0
for page in cfg.get("pages", []):
    for w in page.get("widgets", []):
        if w.get("type") != "html" or w.get("id") == "liquid-glass":
            continue
        html = w.get("options", {}).get("html", "")
        i = html.find(MARK)
        if i >= 0:
            j = html.find("</style>", i)
            if j >= 0:
                w["options"]["html"] = html[:i] + html[j + len("</style>"):]
                removed += 1

# Rounded, borderless cards so the real widgets match the glass panels.
ap = cfg.setdefault("display", {}).setdefault("appearance", {})
ap["radius"] = 30
ap["border"] = False
ap["shadow"] = True

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)
print("glass panels:", panels, "own-glass removed:", removed)
