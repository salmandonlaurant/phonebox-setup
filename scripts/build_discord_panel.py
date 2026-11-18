import json, urllib.request, html

BASE = "http://127.0.0.1:8765"
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))
with urllib.request.urlopen(BASE + "/api/discord", timeout=15) as r:
    dc = json.loads(r.read().decode("utf-8"))

channels = dc["snapshot"]["channels"]
servers = {}
for c in channels:
    gid = c.get("guildId") or c.get("guild") or "other"
    if gid not in servers:
        servers[gid] = {"name": c.get("guild") or "Other", "list": []}
    servers[gid]["list"].append(c)

# ---- shortcuts (hidden VBS wrapper -> dc-ctl.py -> agent RPC) ----
shortcuts = cfg.setdefault("shortcuts", [])
by_id = {s["id"]: s for s in shortcuts}

def add_sid(sid, label, icon, action, chan=""):
    args = '//B "C:\\Users\\Admin\\AppData\\Local\\PhoneBox\\dc-ctl-run.vbs" ' + action
    if chan:
        args += " " + chan
    entry = {"id": sid, "label": label, "icon": icon, "color": "#5865F2",
             "cmd": "C:\\Windows\\System32\\wscript.exe", "args": args, "toggle": False}
    if sid in by_id:
        by_id[sid].update(entry)
    else:
        shortcuts.append(entry)
        by_id[sid] = entry

add_sid("dc-mute", "Mic mute", "🎙️", "mute")
add_sid("dc-deaf", "Deafen", "🎧", "deafen")
add_sid("dc-leave", "Leave voice", "📞", "leave")

for gid, g in servers.items():
    for c in g["list"]:
        add_sid("dc-join-" + c["id"], "Join " + c["name"], "🔊", "join", c["id"])

# ---- HTML control panel ----
groups_html = []
for gid, g in servers.items():
    name = html.escape(g["name"])
    chans = "".join(
        '<button class="ch" data-id="dc-join-%s"><span class="ci">🔊</span><span class="cn">%s</span></button>'
        % (html.escape(c["id"]), html.escape(c["name"]))
        for c in g["list"]
    )
    groups_html.append('<div class="grp"><div class="gn">%s</div><div class="chs">%s</div></div>' % (name, chans))

CSS = """<style>
html,body{margin:0;height:100%;overflow:hidden;font-family:"SF Pro Rounded",Roboto,system-ui,sans-serif;background:transparent;color:#ececf2}
#w{display:flex;flex-direction:column;height:100%;box-sizing:border-box;gap:10px}
#hd{display:flex;align-items:center;gap:9px;flex:0 0 auto}
#lg{width:30px;height:30px;border-radius:50%;background:#5865f2;display:flex;align-items:center;justify-content:center;font-size:17px;color:#fff}
#ti{font-size:18px;font-weight:700}
#sub{font-size:12px;color:#9a9aa6;margin-left:auto}
#ctl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;flex:0 0 auto}
.b{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;min-height:64px;box-sizing:border-box;
   border:1px solid rgba(255,255,255,.12);border-radius:14px;background:rgba(255,255,255,.06);color:#ececf2;font-size:14px;font-weight:600;cursor:pointer}
.b span{font-size:22px}
.b:active{transform:scale(.96);background:rgba(88,101,242,.35)}
#lbl{font-size:12px;color:#9a9aa6;text-transform:uppercase;letter-spacing:.09em;flex:0 0 auto}
#list{flex:1 1 auto;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;display:flex;flex-direction:column;gap:10px;padding:2px 2px 12px}
.grp{background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:8px}
.gn{font-size:12px;font-weight:700;color:#9aa4ff;margin-bottom:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chs{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:6px}
.ch{display:flex;align-items:center;gap:6px;min-width:0;border:1px solid rgba(255,255,255,.09);border-radius:10px;
    background:rgba(255,255,255,.05);color:#ececf2;font:inherit;font-size:13px;padding:8px;cursor:pointer;text-align:left}
.ch:active{transform:scale(.97);background:rgba(88,101,242,.35)}
.ci{font-size:15px;flex:0 0 auto}
.cn{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
</style>"""

BODY = """<div id="w"><div id="hd"><div id="lg">🎮</div><div id="ti">Discord</div><div id="sub">Voice control</div></div>
<div id="ctl"><button class="b" data-id="dc-mute"><span>🎙️</span>Mute</button>
<button class="b" data-id="dc-deaf"><span>🎧</span>Deafen</button>
<button class="b" data-id="dc-leave"><span>📞</span>Leave</button></div>
<div id="lbl">Join a voice channel</div><div id="list">@@GROUPS@@</div></div>
<script>
var list=document.getElementById('list');
var b=document.querySelectorAll('.b,.ch');
for(var i=0;i<b.length;i++)b[i].addEventListener('click',function(){phonebox.run(this.getAttribute('data-id'))});
</script>""".replace("@@GROUPS@@", "".join(groups_html))

HTML = CSS + BODY

work = [p for p in cfg["pages"] if p["id"] == "work"][0]
widgets = work["widgets"]
widgets[:] = [w for w in widgets if w.get("id") not in ("discord-control", "discord-panel")]
panel = {"id": "discord-panel", "type": "html", "x": 0, "y": 0, "w": 7, "h": 6,
         "options": {"html": HTML}}
# insert after liquid-glass
idx = 1 if widgets and widgets[0].get("id") == "liquid-glass" else 0
widgets.insert(idx, panel)

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
print("groups:", len(groups_html), "channels:", len(channels), "html chars:", len(HTML))
print("work widgets:", [(w["id"], w["x"], w["y"], w["w"], w["h"]) for w in widgets])
