import json, os, urllib.request

BASE = "http://127.0.0.1:8765"
TEMP = os.environ["TEMP"]
BRAVE = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
PS = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
HELPER = r"C:\Users\Admin\AppData\Local\PhoneBox\ytm-play.ps1"

# ---------------------------------------------------------------- load songs
songs = json.load(open(os.path.join(TEMP, "phonebox-home-songs.json"), encoding="utf-8"))
fix = {"COMÃ‹ N GO": "COMË N GO"}
for s in songs:
    s["title"] = fix.get(s["title"], s["title"])

# ---------------------------------------------------------------- fetch settings
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

# ---------------------------------------------------------------- shortcuts
cfg["shortcuts"] = [s for s in cfg.get("shortcuts", []) if not str(s.get("id", "")).startswith("ytm-")]
for n, s in enumerate(songs, 1):
    cfg["shortcuts"].append({
        "id": f"ytm-{n:02d}",
        "label": s["title"],
        "icon": "\u266a",
        "color": "#FF0033",
        "cmd": PS,
        "args": f'-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "{HELPER}" -VideoId "{s["id"]}"',
        "toggle": False,
    })

# ---------------------------------------------------------------- picker HTML
songs_js = json.dumps(
    [{"i": f"ytm-{n:02d}", "n": f"{n:02d}", "t": s["title"]} for n, s in enumerate(songs, 1)],
    ensure_ascii=False,
)

html = """<style>
#wrap{display:flex;flex-direction:column;height:100%;box-sizing:border-box}
#head{flex:0 0 auto;padding:6px 8px 5px}
#ttl{font-size:12px;font-weight:700;color:#fff;letter-spacing:.03em;margin-bottom:5px}
#f{width:100%;box-sizing:border-box;padding:7px 9px;border-radius:8px;border:1px solid #3a3a42;background:#1a1a1f;color:#eef2f6;font-size:13px;outline:none}
#f:focus{border-color:#ff0033}
#list{flex:1 1 auto;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:0 6px 8px;box-sizing:border-box}
.s{display:block;width:100%;text-align:left;border:0;border-radius:8px;background:#24242a;color:#f2f2f5;padding:9px 10px;margin-bottom:5px;font-size:12px;line-height:1.3;cursor:pointer}
.s:active,.s.hit{background:#ff0033;color:#fff}
.s i{display:inline-block;width:20px;color:#8a94a3;font-style:normal;font-size:10px}
.none{color:#8a94a3;font-size:12px;padding:10px 4px}
</style>
<div id="wrap">
<div id="head"><div id="ttl">YouTube Music &middot; Home</div><input id="f" type="search" placeholder="Filter songs\u2026" autocomplete="off" spellcheck="false"></div>
<div id="list"></div>
</div>
<script>
var S=SONGS_JS;
var L=document.getElementById('list'),F=document.getElementById('f');
function esc(x){return String(x).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function draw(q){q=(q||'').toLowerCase().trim();var a=S.filter(function(s){return !q||s.t.toLowerCase().indexOf(q)>=0});
if(!a.length){L.innerHTML='<div class="none">No songs match</div>';return}
L.innerHTML=a.map(function(s){return '<button class="s" data-id="'+s.i+'"><i>'+s.n+'</i>'+esc(s.t)+'</button>'}).join('');
var b=L.querySelectorAll('.s');for(var i=0;i<b.length;i++)b[i].addEventListener('click',function(){var el=this;el.classList.add('hit');setTimeout(function(){el.classList.remove('hit')},250);phonebox.run(el.getAttribute('data-id'))})}
F.addEventListener('input',function(){draw(this.value)});draw('');
</script>""".replace("SONGS_JS", songs_js)

# ---------------------------------------------------------------- page 'ai'
for page in cfg.get("pages", []):
    if page.get("id") == "ai":
        page["title"] = "Music"
        page["widgets"] = [
            {
                "id": "ytm-picker",
                "type": "html",
                "x": 0, "y": 0, "w": 7, "h": 6,
                "options": {"html": html, "transparent": False},
            },
            {
                "id": "music-now-playing",
                "type": "media",
                "x": 7, "y": 0, "w": 5, "h": 6,
            },
        ]
        break
else:
    raise SystemExit("page id 'ai' not found")

# ---------------------------------------------------------------- PUT settings
body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(
    BASE + "/api/settings",
    data=body,
    method="PUT",
    headers={"Content-Type": "application/json; charset=utf-8"},
)
with urllib.request.urlopen(req, timeout=20) as r:
    print("PUT settings:", r.status, r.read().decode("utf-8", "replace")[:200])

# ---------------------------------------------------------------- refresh
req = urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST")
with urllib.request.urlopen(req, timeout=20) as r:
    print("refresh:", r.status, r.read().decode("utf-8", "replace")[:200])

print("shortcuts:", len(cfg["shortcuts"]), "| ytm:", sum(1 for s in cfg["shortcuts"] if str(s.get("id", "")).startswith("ytm-")))
print("picker html chars:", len(html))
