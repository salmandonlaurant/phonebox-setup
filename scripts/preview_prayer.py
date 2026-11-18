import json
c = json.load(open(r"C:\Users\Admin\AppData\Roaming\PhoneBox\config.json", encoding="utf-8"))
p = [x for x in c["pages"] if x["id"] == "home"][0]
h = [w for w in p["widgets"] if w["id"] == "prayer"][0]["options"]["html"]
wrap = """<!doctype html><html><head><meta charset="utf-8"></head>
<body style="margin:0;background:#07070b"><div style="width:200px;height:120px;border:1px solid #333;border-radius:18px;overflow:hidden;padding:6px">""" + h + "</div></body></html>"
open(r"C:\Users\Admin\AppData\Local\Temp\opencode\preview-prayer.html", "w", encoding="utf-8").write(wrap)
print("ok")
