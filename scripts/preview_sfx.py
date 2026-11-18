import json
c = json.load(open(r"C:\Users\Admin\AppData\Roaming\PhoneBox\config.json", encoding="utf-8"))
w = [p for p in c["pages"] if p["id"] == "work"][0]
h = [x for x in w["widgets"] if x["id"] == "discord-sfx"][0]["options"]["html"]
# Wrap so it renders at the A32's ~5-column CSS width / full page height.
wrap = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>html,body{margin:0;background:#07070b;display:flex;align-items:center;justify-content:center;height:100vh}
#dev{width:330px;height:360px;background:rgba(255,255,255,.02);border:1px solid #333;border-radius:22px;overflow:hidden}</style></head>
<body><div id="dev">""" + h + "</div></body></html>"
open(r"C:\Users\Admin\AppData\Local\Temp\opencode\preview-sfx.html", "w", encoding="utf-8").write(wrap)
print("ok")
