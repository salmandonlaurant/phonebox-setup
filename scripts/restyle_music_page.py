import json, os, urllib.request

BASE = "http://127.0.0.1:8765"
TEMP = os.environ["TEMP"]
VBS = r"C:\Users\Admin\AppData\Local\PhoneBox\ytm-run.vbs"

songs = json.load(open(os.path.join(TEMP, "phonebox-home-songs.json"), encoding="utf-8"))
fix = {"COMÃ‹ N GO": "COMË N GO"}
for s in songs:
    s["title"] = fix.get(s["title"], s["title"])

with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

# All song buttons now go through the hidden VBScript -> PowerShell helper.
for sc in cfg.get("shortcuts", []):
    if str(sc.get("id", "")).startswith("ytm-"):
        n = int(sc["id"][4:])
        sc["cmd"] = r"C:\Windows\System32\wscript.exe"
        sc["args"] = f'//B "{VBS}" "{songs[n - 1]["id"]}"'

songs_js = json.dumps(
    [{"i": f"ytm-{n:02d}", "v": s["id"], "t": s["title"]} for n, s in enumerate(songs, 1)],
    ensure_ascii=False,
)

html = """<style>
:root{--acc:#ff0033;--txt:#ececf0;--sub:#94949e;--card:rgba(255,255,255,.045);--line:rgba(255,255,255,.07)}
#wrap{display:flex;flex-direction:column;height:100%;box-sizing:border-box;gap:8px}
#hd{flex:0 0 auto}
#brand{display:flex;align-items:center;gap:8px;margin-bottom:8px}
#logo{width:22px;height:22px;border-radius:50%;background:var(--acc);display:flex;align-items:center;justify-content:center;font-size:12px;color:#fff;box-shadow:0 2px 10px rgba(255,0,51,.35)}
#bt{font-size:14px;font-weight:600;letter-spacing:-.01em;color:var(--txt)}
#ct{font-size:10px;color:var(--sub);margin-left:auto;padding-right:2px}
#f{width:100%;box-sizing:border-box;padding:8px 12px;border-radius:20px;border:1px solid var(--line);background:var(--card);color:var(--txt);font-size:12px;outline:none;transition:border-color .2s,background .2s}
#f::placeholder{color:var(--sub)}
#f:focus{border-color:rgba(255,0,51,.6);background:rgba(255,255,255,.07)}
#sect{font-size:10px;color:var(--sub);text-transform:uppercase;letter-spacing:.09em;padding:2px 4px 0}
#list{flex:1 1 auto;overflow-y:auto;-webkit-overflow-scrolling:touch;display:flex;flex-direction:column;gap:5px;padding:2px 2px 10px}
.s{display:flex;align-items:center;gap:10px;width:100%;text-align:left;border:1px solid transparent;border-radius:10px;background:transparent;color:var(--txt);padding:6px 8px;cursor:pointer;transition:background .18s,border-color .18s,transform .12s}
.s:hover{background:var(--card)}
.s:active,.s.hit{background:rgba(255,0,51,.16);border-color:rgba(255,0,51,.35);transform:scale(.985)}
.th{width:46px;height:46px;flex:0 0 auto;border-radius:8px;object-fit:cover;background:#23232a}
.ph{width:46px;height:46px;flex:0 0 auto;border-radius:8px;background:linear-gradient(145deg,#2a2a33,#1c1c23);display:flex;align-items:center;justify-content:center;font-size:16px;color:#666}
.meta{min-width:0;flex:1 1 auto}
.tt{font-size:12px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.35}
.st{font-size:10px;color:var(--sub);margin-top:2px}
.pl{width:20px;flex:0 0 auto;text-align:center;color:var(--sub);font-size:13px}
.s:active .pl,.s.hit .pl{color:var(--acc)}
.none{color:var(--sub);font-size:12px;padding:14px 6px;text-align:center}
</style>
<div id="wrap">
<div id="hd">
<div id="brand"><div id="logo">♫</div><div id="bt">YouTube Music</div><div id="ct"></div></div>
<input id="f" type="search" placeholder="Search songs" autocomplete="off" spellcheck="false">
<div id="sect">Home mix</div>
</div>
<div id="list"></div>
</div>
<script>
var S=SONGS_JS;
var L=document.getElementById('list'),F=document.getElementById('f');
document.getElementById('ct').textContent=S.length+' songs';
function esc(x){return String(x).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function draw(q){q=(q||'').toLowerCase().trim();var a=S.filter(function(s){return !q||s.t.toLowerCase().indexOf(q)>=0});
if(!a.length){L.innerHTML='<div class="none">No songs found</div>';return}
L.innerHTML=a.map(function(s){return '<button class="s" data-id="'+s.i+'"><img class="th" loading="lazy" referrerpolicy="no-referrer" src="https://i.ytimg.com/vi/'+s.v+'/mqdefault.jpg" alt=""><div class="meta"><div class="tt">'+esc(s.t)+'</div><div class="st">Song &middot; YouTube Music</div></div><div class="pl">&#9654;</div></button>'}).join('');
var imgs=L.querySelectorAll('img.th');for(var i=0;i<imgs.length;i++)imgs[i].addEventListener('error',function(){var p=document.createElement('div');p.className='ph';p.textContent='♫';this.parentNode.insertBefore(p,this);this.remove()});
var b=L.querySelectorAll('.s');for(var j=0;j<b.length;j++)b[j].addEventListener('click',function(){var el=this;el.classList.add('hit');setTimeout(function(){el.classList.remove('hit')},300);phonebox.run(el.getAttribute('data-id'))})}
F.addEventListener('input',function(){draw(this.value)});draw('');
</script>""".replace("SONGS_JS", songs_js)

for page in cfg.get("pages", []):
    if page.get("id") == "ai":
        for w in page["widgets"]:
            if w["id"] == "ytm-picker":
                w["options"]["html"] = html
        break

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=20) as r:
    print("PUT:", r.status)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)
print("html chars:", len(html))
