"""Replace the Home media widget with a custom one: no volume/voice control,
album art + track info + progress + transport, and a small orange cat that
dances only while music is playing.
"""
import html
import json
import urllib.request

BASE = "http://127.0.0.1:8765"

WIDGET = r"""<style>
html,body{margin:0;height:100%;overflow:hidden;background:transparent;color:#eef2f6;
  font-family:"SF Pro Rounded",Roboto,system-ui,sans-serif;-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}
#w{display:flex;flex-direction:column;height:100%;box-sizing:border-box;padding:14px 16px 12px;gap:10px;
   border-radius:22px;background:linear-gradient(145deg,rgba(26,28,37,.74),rgba(11,12,17,.8));
   border:1px solid rgba(255,255,255,.07);box-shadow:inset 0 1px 0 rgba(255,255,255,.06)}
#top{display:flex;align-items:center;gap:16px;flex:1 1 auto;min-height:0}
#art{width:clamp(84px,17%,132px);aspect-ratio:1;flex:0 0 auto;border-radius:17px;object-fit:cover;background:#191a22;opacity:0;transition:opacity .35s}
#art.on{opacity:1}
#artph{position:absolute;width:clamp(84px,17%,132px);aspect-ratio:1;border-radius:17px;background:#191a22;
  display:flex;align-items:center;justify-content:center;font-size:40px;color:#4a4d5c;pointer-events:none}
#artph.hide{display:none}
#artbox{position:relative;flex:0 0 auto}
#txt{flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:4px}
#app{display:inline-flex;align-items:center;gap:6px;align-self:flex-start;font-size:12px;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;color:#ff6b6b;background:rgba(255,59,48,.12);border:1px solid rgba(255,59,48,.22);
  padding:3px 9px;border-radius:999px;max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#title{font-size:clamp(19px,3vw,29px);font-weight:780;line-height:1.15;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#artist{font-size:clamp(12px,1.9vw,16px);color:#a9acbb;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#state{font-size:12px;color:#7f8496;display:flex;align-items:center;gap:6px;margin-top:2px}
#dot{width:7px;height:7px;border-radius:50%;background:#55586a}
#dot.live{background:#22c55e;box-shadow:0 0 9px #22c55e;animation:pulse 1.2s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}

/* ---- small orange cat ---- */
#catwrap{position:relative;flex:0 0 116px;width:116px;height:116px;pointer-events:none}
.cat{position:absolute;left:5px;top:15px;width:106px;height:94px;transform-origin:53px 80px}
.cat .tail{position:absolute;left:8px;bottom:13px;width:40px;height:14px;border:7px solid #f59e0b;
  border-left-color:transparent;border-bottom-color:transparent;border-radius:50%;transform-origin:100% 100%;z-index:1}
.cat .body{position:absolute;left:30px;top:42px;width:46px;height:38px;background:#f59e0b;border-radius:44% 44% 46% 46%;z-index:2}
.cat .stripe{position:absolute;background:#e0860a;border-radius:5px;opacity:.75}
.cat .st1{top:7px;left:13px;width:5px;height:14px;transform:rotate(12deg)}
.cat .st2{top:9px;left:26px;width:5px;height:12px;transform:rotate(-10deg)}
.cat .arm{position:absolute;top:5px;width:12px;height:27px;background:#f59e0b;border-radius:9px;transform-origin:50% 11px;z-index:1}
.cat .al{left:-8px}.cat .ar{right:-8px}
.cat .leg{position:absolute;bottom:-5px;width:15px;height:13px;background:#f59e0b;border-radius:0 0 9px 9px}
.cat .ll{left:4px}.cat .lr{right:4px}
.cat .head{position:absolute;left:28px;top:2px;width:50px;height:44px;background:#f59e0b;border-radius:50% 50% 46% 46%;z-index:3}
.cat .ear{position:absolute;top:-9px;width:0;height:0;border-left:11px solid transparent;border-right:11px solid transparent;
  border-bottom:18px solid #f59e0b;filter:drop-shadow(0 -1px 0 #d97706)}
.cat .el{left:0;transform:rotate(-14deg)}.cat .er{right:0;transform:rotate(14deg)}
.cat .hs{position:absolute;top:3px;width:5px;height:17px;background:#e0860a;border-radius:5px;opacity:.7}
.cat .h1{left:20px;transform:rotate(-8deg)}.cat .h2{right:20px;transform:rotate(8deg)}
.cat .eye{position:absolute;top:19px;width:7px;height:9px;background:#2b1b09;border-radius:50% 50% 45% 45%;transition:all .25s}
.cat .eye.l2{left:12px}.cat .eye.r2{right:12px}
.cat .nose{position:absolute;top:28px;left:50%;margin-left:-4px;width:0;height:0;border-left:4px solid transparent;
  border-right:4px solid transparent;border-top:5px solid #e8797e}
.cat .wk{position:absolute;top:30px;width:13px;height:1.5px;background:rgba(255,255,255,.8);border-radius:2px}
.cat .w1{left:1px;transform:rotate(-9deg)}.cat .w2{left:0;transform:rotate(6deg)}
.cat .w3{right:1px;transform:rotate(9deg)}.cat .w4{right:0;transform:rotate(-6deg)}
.cat.sleep .eye{height:3px;top:23px;border-radius:4px}
#notes{position:absolute;inset:0;opacity:0;transition:opacity .3s}
#zzz{position:absolute;right:2px;top:0;font-size:15px;font-weight:800;color:#c9cbd8;opacity:0;transition:opacity .3s}
.note{position:absolute;color:#ffb04a;font-size:19px;font-weight:800;opacity:0}
.n1{left:6px;top:34px}.n2{right:6px;top:16px;font-size:16px}.n3{left:34px;top:2px;font-size:14px}
.playing-on #notes{opacity:1}
.playing-on .note{animation:noteUp 1.5s ease-out infinite}
.playing-on .n2{animation-delay:.5s}.playing-on .n3{animation-delay:1s}
.sleeping-on #zzz{opacity:1;animation:zfloat 2.2s ease-in-out infinite}
@keyframes noteUp{0%{opacity:0;transform:translateY(8px) scale(.7)}25%{opacity:1}100%{opacity:0;transform:translateY(-46px) scale(1.15)}}
@keyframes zfloat{0%,100%{transform:translateY(0);opacity:.35}50%{transform:translateY(-7px);opacity:1}}
@keyframes hop{0%{transform:translateY(0) rotate(-7deg)}100%{transform:translateY(-11px) rotate(7deg)}}
@keyframes armL{0%{transform:rotate(38deg)}100%{transform:rotate(-58deg)}}
@keyframes armR{0%{transform:rotate(-38deg)}100%{transform:rotate(58deg)}}
@keyframes legL{0%{transform:translateY(0)}100%{transform:translateY(-8px)}}
@keyframes legR{0%{transform:translateY(-8px)}100%{transform:translateY(0)}}
@keyframes wag{0%{transform:rotate(-24deg)}100%{transform:rotate(24deg)}}
@keyframes twitch{0%{transform:rotate(-14deg) scaleY(1)}100%{transform:rotate(-5deg) scaleY(1.14)}}
@keyframes breathe{0%{transform:scaleY(1)}100%{transform:scaleY(1.05)}}
.cat.dance{animation:hop .46s ease-in-out infinite alternate}
.cat.dance .al{animation:armL .46s ease-in-out infinite alternate}
.cat.dance .ar{animation:armR .46s ease-in-out infinite alternate}
.cat.dance .ll{animation:legL .3s ease-in-out infinite alternate}
.cat.dance .lr{animation:legR .3s ease-in-out infinite alternate}
.cat.dance .tail{animation:wag .38s ease-in-out infinite alternate}
.cat.dance .el{animation:twitch .55s ease-in-out infinite alternate}
.cat.sleep{animation:breathe 2.4s ease-in-out infinite alternate}

/* ---- progress + transport ---- */
#prog{display:flex;flex-direction:column;gap:5px;flex:0 0 auto}
#bar{height:6px;border-radius:6px;background:rgba(255,255,255,.09);overflow:hidden}
#fill{height:100%;width:0;border-radius:6px;background:linear-gradient(90deg,#ff3b30,#ff8a3d);transition:width .12s linear}
#times{display:flex;justify-content:space-between;font-size:12px;color:#9a9eaf;font-variant-numeric:tabular-nums}
#ctl{display:flex;align-items:center;justify-content:center;gap:10px;flex:0 0 auto}
button{display:flex;align-items:center;justify-content:center;border:1px solid rgba(255,255,255,.1);border-radius:14px;
  background:rgba(255,255,255,.06);color:#eef2f6;cursor:pointer;-webkit-tap-highlight-color:transparent}
button:active{transform:scale(.93);background:rgba(255,59,48,.3)}
.ic{width:54px;height:46px;font-size:19px}
.seek{width:58px;height:46px;font-size:13px;font-weight:700;color:#c7cad6}
.play{width:68px;height:52px;border-radius:17px;background:linear-gradient(145deg,#ff4438,#e01f18);
  border-color:rgba(255,255,255,.18);box-shadow:0 5px 14px rgba(255,59,48,.28);font-size:24px}
svg{width:19px;height:19px;fill:currentColor}
.play svg{width:24px;height:24px}
</style>
<div id="w">
  <div id="top">
    <div id="artbox"><div id="artph">♪</div><img id="art" alt=""></div>
    <div id="txt">
      <div id="app">Media</div>
      <div id="title">Nothing playing</div>
      <div id="artist">Start music on the PC</div>
      <div id="state"><span id="dot"></span><span id="statetxt">Idle</span></div>
    </div>
    <div id="catwrap">
      <div class="cat sleep" id="cat">
        <div class="tail"></div>
        <div class="body"><div class="stripe st1"></div><div class="stripe st2"></div>
          <div class="arm al"></div><div class="arm ar"></div><div class="leg ll"></div><div class="leg lr"></div></div>
        <div class="head">
          <div class="ear el"></div><div class="ear er"></div><div class="hs h1"></div><div class="hs h2"></div>
          <div class="eye l2"></div><div class="eye r2"></div><div class="nose"></div>
          <div class="wk w1"></div><div class="wk w2"></div><div class="wk w3"></div><div class="wk w4"></div>
        </div>
      </div>
      <div id="notes"><span class="note n1">♪</span><span class="note n2">♫</span><span class="note n3">♪</span></div>
      <div id="zzz">z Z z</div>
    </div>
  </div>
  <div id="prog"><div id="bar"><div id="fill"></div></div>
    <div id="times"><span id="pos">0:00</span><span id="dur">0:00</span></div></div>
  <div id="ctl">
    <button class="seek" data-run="mp-back10" aria-label="Back 10 seconds">−10s</button>
    <button class="ic" data-run="mp-prev" aria-label="Previous"><svg viewBox="0 0 24 24"><path d="M6 5h2v14H6zM20 5v14L9.5 12z"/></svg></button>
    <button class="play" data-run="mp-play" aria-label="Play or pause"><svg id="ppicon" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></button>
    <button class="ic" data-run="mp-next" aria-label="Next"><svg viewBox="0 0 24 24"><path d="M16 5h2v14h-2zM4 5v14l10.5-7z"/></svg></button>
    <button class="seek" data-run="mp-fwd10" aria-label="Forward 10 seconds">+10s</button>
  </div>
</div>
<script>
(function(){
 var $=function(id){return document.getElementById(id)};
 var cat=$('cat'),cw=$('catwrap'),art=$('art'),artph=$('artph');
 var title=$('title'),artist=$('artist'),app=$('app'),dot=$('dot'),statetxt=$('statetxt');
 var fill=$('fill'),posEl=$('pos'),durEl=$('dur'),ppicon=$('ppicon');
 var M=null,basePos=0,baseAt=0,dur=0,lastArt=-1;
 var PATH_PLAY='M8 5v14l11-7z',PATH_PAUSE='M7 5h4v14H7zM13 5h4v14h-4z';
 function fmt(ms){if(!isFinite(ms)||ms<0)ms=0;var s=Math.floor(ms/1000);return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
 function paint(m){
   M=m||null;
   if(!m){
     title.textContent='Nothing playing';artist.textContent='Start music on the PC';app.textContent='Media';
     statetxt.textContent='Idle';dot.classList.remove('live');
     fill.style.width='0';posEl.textContent='0:00';durEl.textContent='0:00';
     ppicon.innerHTML='<path d="'+PATH_PLAY+'"/>';basePos=0;baseAt=performance.now();dur=0;
     art.classList.remove('on');artph.classList.remove('hide');lastArt=-1;
     cat.className='cat sleep';cw.className='';return;
   }
   title.textContent=m.title||'Unknown track';
   artist.textContent=[m.artist,m.album].filter(Boolean).join(' · ')||'—';
   app.textContent=m.app||'Media';
   statetxt.textContent=m.playing?'Now playing':'Paused';
   dot.classList.toggle('live',!!m.playing);
   ppicon.innerHTML='<path d="'+(m.playing?PATH_PAUSE:PATH_PLAY)+'"/>';
   if(m.artId&&m.artId!==lastArt){art.src='/agent/api/art?id='+m.artId;art.classList.add('on');artph.classList.add('hide');lastArt=m.artId}
   else if(!m.artId){art.classList.remove('on');artph.classList.remove('hide');lastArt=-1}
   basePos=m.posMs||0;baseAt=performance.now();dur=m.durMs||0;
   cat.className='cat '+(m.playing?'dance':'sleep');
   cw.className=m.playing?'playing-on':'sleeping-on';
 }
 function loop(){
   if(M&&dur>0){
     var p=basePos+(M.playing?performance.now()-baseAt:0);if(p>dur)p=dur;
     fill.style.width=(p/dur*100)+'%';posEl.textContent=fmt(p);durEl.textContent=fmt(dur);
   }else if(M){
     fill.style.width=M.playing?'100%':'0';posEl.textContent=fmt(M.posMs||0);durEl.textContent=M.playing?'LIVE':'0:00';
   }
   requestAnimationFrame(loop);
 }
 var bs=document.querySelectorAll('[data-run]');
 for(var i=0;i<bs.length;i++)bs[i].addEventListener('click',function(){phonebox.run(this.getAttribute('data-run'))});
 phonebox.on('state',function(s){paint(s&&s.media)});
 loop();
})();
</script>"""

# ---- hidden media-control shortcuts ----
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

shortcuts = cfg.setdefault("shortcuts", [])
by_id = {s["id"]: s for s in shortcuts}

def add_sid(sid, label, icon, arg):
    entry = {
        "id": sid, "label": label, "icon": icon, "color": "#ff3b30",
        "cmd": "C:\\Windows\\System32\\wscript.exe",
        "args": '//B "C:\\Users\\Admin\\AppData\\Local\\PhoneBox\\agent-post-run.vbs" ' + arg,
        "toggle": False,
    }
    if sid in by_id:
        by_id[sid].update(entry)
    else:
        shortcuts.append(entry)
        by_id[sid] = entry

add_sid("mp-play",  "Play / Pause", "⏯", "api/media/playpause")
add_sid("mp-next",  "Next track",   "⏭", "api/media/next")
add_sid("mp-prev",  "Previous",     "⏮", "api/media/prev")
add_sid("mp-back10","Back 10s",     "⏪", "seekrel:-10000")
add_sid("mp-fwd10", "Forward 10s",  "⏩", "seekrel:10000")

# ---- replace the Home media widget ----
home = [p for p in cfg["pages"] if p["id"] == "home"][0]
widgets = home["widgets"]
old = next((w for w in widgets if w.get("id") == "media"), None)
pos = widgets.index(old) if old else 1
widgets[:] = [w for w in widgets if w.get("id") not in ("media", "media-cat")]
new = {
    "id": "media-cat", "type": "html",
    "x": old.get("x", 6) if old else 6,
    "y": old.get("y", 0) if old else 0,
    "w": old.get("w", 6) if old else 6,
    "h": old.get("h", 4) if old else 4,
    "options": {"html": WIDGET, "transparent": True},
    "appearance": {"style": "borderless", "radius": 0, "padding": 0, "border": False, "shadow": False},
}
widgets.insert(min(pos, len(widgets)), new)

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
print("home:", [(w["id"], w["type"], w["x"], w["y"], w["w"], w["h"]) for w in widgets])
print("media shortcuts:", [s["id"] for s in shortcuts if s["id"].startswith("mp-")])
print("widget html chars:", len(WIDGET))

# Preview file for visual verification
prelude = """<script>window.phonebox={data:{state:{media:{app:"YouTube Music",title:"4AM",artist:"Nemzzz",album:"4AM",playing:true,posMs:64000,durMs:155881,artId:132}}},on:function(k,f){if(k==='state')f(this.data.state)},run:function(id){console.log('RUN',id)}};</script>"""
wrap = ('<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;background:#07070b">'
        + prelude + '<div style="width:790px;height:430px;border:1px solid #222;border-radius:22px;overflow:hidden">'
        + WIDGET + '</div></body></html>')
with open(r"C:\Users\Admin\AppData\Local\Temp\opencode\preview-media-cat.html", "w", encoding="utf-8") as f:
    f.write(wrap)
print("preview written")
