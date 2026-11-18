import json
c = json.load(open(r"C:\Users\Admin\AppData\Roaming\PhoneBox\config.json", encoding="utf-8"))
p = [x for x in c["pages"] if x["id"] == "work"][0]
h = [w for w in p["widgets"] if w["id"] == "discord-panel"][0]["options"]["html"]
prelude = """<script>window.phonebox={run:function(id){console.log('RUN',id)}};</script>"""
wrap = """<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;background:#07070b">""" + prelude + """<div id="dev" style="width:460px;height:360px;border:1px solid #333;border-radius:22px;overflow:hidden">""" + h + "</div></body></html>"
open(r"C:\Users\Admin\AppData\Local\Temp\opencode\preview-discord-panel.html", "w", encoding="utf-8").write(wrap)
print("ok")
