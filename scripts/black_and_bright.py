import base64, io, json, urllib.request
from PIL import Image, ImageFilter, ImageDraw

BASE = "http://127.0.0.1:8765"

# ---- dark base for the frosted panels (no wallpaper) ----
W, H = 960, 540
base = Image.new("RGB", (W, H), (4, 5, 8))
d = ImageDraw.Draw(base)
for cy, cx, rgb, r in [
    (0.20, 0.15, (22, 34, 52), 430),
    (0.85, 0.80, (16, 24, 40), 400),
    (0.55, 0.50, (10, 16, 28), 520),
]:
    x, y = int(cx * W), int(cy * H)
    for i in range(r, 0, -12):
        a = 1 - i / r
        col = tuple(int(v * a) for v in rgb)
        d.ellipse([x - i, y - i, x + i, y + i], fill=col)
base = base.filter(ImageFilter.GaussianBlur(40))
buf = io.BytesIO()
base.save(buf, "JPEG", quality=70, optimize=True)
BLUR = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
print("dark glass base:", len(BLUR), "chars")

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
    widgets = page.get("widgets", [])
    # remove the synced PC wallpaper entirely
    widgets[:] = [w for w in widgets if w.get("id") not in ("pc-wallpaper", "liquid-glass")]

    divs = []
    for w in widgets:
        if w.get("id") == "liquid-glass":
            continue
        x, y = int(w.get("x", 0)), int(w.get("y", 0))
        ww, hh = int(w.get("w", 1)), int(w.get("h", 1))
        sx = 12.0 / ww * 100 if ww else 100
        sy = 6.0 / hh * 100 if hh else 100
        px = pct(x, 12 - ww) if ww < 12 else 0
        py = pct(y, 6 - hh) if hh < 6 else 0
        style = (f"grid-area:{y+1}/{x+1}/span {hh}/span {ww};"
                 f"background-image:url('{BLUR}');"
                 f"background-size:{sx:.3f}% {sy:.3f}%;"
                 f"background-position:{px:.3f}% {py:.3f}%")
        divs.append(f'<div class="g" style="{style}"></div>')
    if not divs:
        continue
    html = CSS + '<div id="g">' + "".join(divs) + "</div>"
    widgets.insert(0, {
        "id": "liquid-glass", "type": "html",
        "x": 0, "y": 0, "w": 12, "h": 6,
        "options": {"html": html, "transparent": True},
        "appearance": {"style": "borderless", "radius": 0, "padding": 0,
                       "border": False, "shadow": False},
    })

# ---- always-on, high brightness ----
cfg.setdefault("night", {})["enabled"] = False
cfg["night"]["brightness"] = 1.0
d = cfg.setdefault("display", {})
d["keepAwake"] = True
d["idleDimMin"] = 0
d["nightWhenDark"] = False
d["autoBrightness"] = False
d["proximityWake"] = False
d["theme"] = "amoled"

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)
print("pages updated:", len(cfg.get("pages", [])))
