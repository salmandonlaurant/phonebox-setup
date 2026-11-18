import json, os, urllib.request

BASE = "http://127.0.0.1:8765"
VBS = r"C:\Users\Admin\AppData\Local\PhoneBox\dc-sfx-run.vbs"
sounds = json.load(open(os.path.join(os.environ["TEMP"], "phonebox-discord-sounds.json"), encoding="utf-8"))

EMOJI = {
    "quack": "\U0001F986", "airhorn": "\U0001F4E2", "cricket": "\U0001F997",
    "golf clap": "\U0001F44F", "sad horn": "\U0001F622", "ba dum tss": "\U0001F941",
    "laugh": "\U0001F602", "Creeper": "\U0001F47B", "flashbang for the ears": "\U0001F4A5",
    "discord join": "\u27A1\uFE0F", "discord leave": "\u2B05\uFE0F", "5 Sekunden": "\u23F1\uFE0F",
    "where your momm attt": "\U0001F4E3", "anitamaxwin": "\U0001F3C6", "OhMahGod": "\U0001F631",
    "Embarrassing": "\U0001F633", "Dirty Foreigner": "\U0001F3A4", "Open na noor": "\U0001F3B5",
}

with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

# One hidden shortcut per sound.
for n, s in enumerate(sounds, 1):
    sid = f"sfx-{n:02d}"
    existing = next((x for x in cfg["shortcuts"] if x.get("id") == sid), None)
    entry = {
        "id": sid,
        "label": s["name"],
        "icon": EMOJI.get(s["name"], "\U0001F50A"),
        "color": "#5865F2",
        "cmd": r"C:\Windows\System32\wscript.exe",
        "args": f'//B "{VBS}" {s["sound_id"]} {s.get("guild_id", 0)}',
        "toggle": False,
    }
    if existing:
        existing.update(entry)
    else:
        cfg["shortcuts"].append(entry)

items = json.dumps(
    [{"i": f"sfx-{n:02d}", "n": s["name"], "e": EMOJI.get(s["name"], "\U0001F50A")}
     for n, s in enumerate(sounds, 1)],
    ensure_ascii=False,
)

html = """<style>
:root{--ac:#5865f2;--txt:#ececf2;--sub:#9a9aa6;--card:rgba(255,255,255,.045);--line:rgba(255,255,255,.07)}
#wrap{display:flex;flex-direction:column;height:100%;box-sizing:border-box;gap:8px}
#hd{flex:0 0 auto}
#brand{display:flex;align-items:center;gap:8px;margin-bottom:8px}
#logo{width:22px;height:22px;border-radius:50%;background:var(--ac);display:flex;align-items:center;justify-content:center;font-size:12px;color:#fff}
#bt{font-size:14px;font-weight:600;letter-spacing:-.01em;color:var(--txt)}
#ct{font-size:10px;color:var(--sub);margin-left:auto}
#f{width:100%;box-sizing:border-box;padding:8px 12px;border-radius:20px;border:1px solid var(--line);background:var(--card);color:var(--txt);font-size:12px;outline:none}
#f::placeholder{color:var(--sub)}
#f:focus{border-color:rgba(88,101,242,.7);background:rgba(255,255,255,.07)}
#list{flex:1 1 auto;overflow-y:auto;-webkit-overflow-scrolling:touch;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;padding:2px 2px 10px}
.s{display:flex;align-items:center;gap:7px;min-width:0;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--txt);padding:8px;cursor:pointer;text-align:left;transition:background .18s,border-color .18s,transform .12s}
.s:hover{background:rgba(88,101,242,.14)}
.s:active,.s.hit{background:rgba(88,101,242,.3);border-color:rgba(88,101,242,.65);transform:scale(.97)}
.e{font-size:15px;flex:0 0 auto;width:20px;text-align:center}
.n{font-size:11px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.none{grid-column:1/-1;color:var(--sub);font-size:12px;text-align:center;padding:14px}
</style>
<div id="wrap"><div id="hd"><div id="brand"><div id="logo">\u266a</div><div id="bt">Soundboard</div><div id="ct"></div></div>
<input id="f" type="search" placeholder="Search sounds" autocomplete="off" spellcheck="false"></div><div id="list"></div></div>
<script>
var S=ITEMS;var L=document.getElementById('list'),F=document.getElementById('f');
document.getElementById('ct').textContent=S.length+' sounds';
function esc(x){return String(x).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function draw(q){q=(q||'').toLowerCase().trim();var a=S.filter(function(s){return !q||s.n.toLowerCase().indexOf(q)>=0});
if(!a.length){L.innerHTML='<div class="none">No sounds found</div>';return}
L.innerHTML=a.map(function(s){return '<button class="s" data-id="'+s.i+'"><span class="e">'+s.e+'</span><span class="n">'+esc(s.n)+'</span></button>'}).join('');
var b=L.querySelectorAll('.s');for(var i=0;i<b.length;i++)b[i].addEventListener('click',function(){var el=this;el.classList.add('hit');setTimeout(function(){el.classList.remove('hit')},280);phonebox.run(el.getAttribute('data-id'))})}
F.addEventListener('input',function(){draw(this.value)});draw('');
</script>""".replace("ITEMS", items)

for page in cfg.get("pages", []):
    if page.get("id") != "work":
        continue
    page["title"] = "Discord"
    page["widgets"] = [
        {
            "id": "discord-control", "type": "discord",
            "x": 0, "y": 0, "w": 8, "h": 6,
            "options": {"channels": True, "notifications": True, "control": True},
        },
        {
            "id": "discord-sfx", "type": "html",
            "x": 8, "y": 0, "w": 4, "h": 6,
            "options": {"html": html},
        },
    ]
    break
else:
    raise SystemExit("page work not found")

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=20) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)
print("sounds:", len(sounds))
