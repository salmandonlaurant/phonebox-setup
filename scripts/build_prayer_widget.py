import json, urllib.request

BASE = "http://127.0.0.1:8765"
# Riyadh default (system timezone: Arab Standard Time, UTC+3). Change these if the user gives a city.
LAT, LNG, TZ = 24.7136, 46.6753, 3
FAJR_ANGLE, ISHA_MIN = 18.5, 90  # Umm al-Qura (Saudi Arabia)

JS = r"""<style>
html,body{margin:0;height:100%;overflow:hidden;font-family:"SF Pro Rounded",Roboto,system-ui,sans-serif;color:#ececf2;background:transparent}
#p{height:100%;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center;gap:5px;padding:2px 4px}
#nx{display:flex;align-items:baseline;gap:8px;min-width:0}
#ic{font-size:19px;flex:0 0 auto}
#nm{font-size:17px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#tm{margin-left:auto;font-size:17px;font-weight:700;font-variant-numeric:tabular-nums;color:#7dd3fc;flex:0 0 auto}
#in{font-size:11px;color:#9a9aa6;white-space:nowrap}
#all{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px 6px;font-size:11px;color:#c8c9d4}
#all b{color:#8f95a8;font-weight:600}
#all span{font-variant-numeric:tabular-nums}
#bar{height:3px;border-radius:3px;background:rgba(255,255,255,.08);overflow:hidden}
#fill{height:100%;width:0;background:linear-gradient(90deg,#38bdf8,#818cf8);transition:width .8s}
</style>
<div id="p"><div id="nx"><span id="ic">🕌</span><span id="nm">—</span><span id="tm">—</span></div>
<div id="in">&nbsp;</div>
<div id="all"></div><div id="bar"><div id="fill"></div></div></div>
<script>
var LAT=@@LAT@@,LNG=@@LNG@@,TZ=@@TZ@@,FAJRA=@@FAJRA@@,ISHAMIN=@@ISHAMIN@@;
var d2r=Math.PI/180,r2d=180/Math.PI;
function fix(a){while(a<0)a+=360;while(a>=360)a-=360;return a}
function times(date){
 var jd=date.getTime()/86400000+2440587.5,D=jd-2451545.0;
 var g=d2r*fix(357.529+0.98560028*D),q=fix(280.459+0.98564736*D);
 var L=d2r*fix(q+1.915*Math.sin(g)+0.020*Math.sin(2*g));
 var e=d2r*(23.439-0.00000036*D);
 var RA=r2d*Math.atan2(Math.cos(e)*Math.sin(L),Math.cos(L))/15;
 RA=((RA%24)+24)%24;
 var eqt=q/15-RA,dec=r2d*Math.asin(Math.sin(e)*Math.sin(L));
 var mid=12+TZ-LNG/15-eqt;
 function ha(alt,pm){
   var c=(Math.sin(alt*d2r)-Math.sin(LAT*d2r)*Math.sin(dec*d2r))/(Math.cos(LAT*d2r)*Math.cos(dec*d2r));
   if(c<-1||c>1)return NaN;
   return mid+(pm?1:-1)*r2d*Math.acos(c)/15;
 }
 var asrAlt=r2d*Math.atan(1/(1+Math.tan(d2r*Math.abs(LAT-dec))));
 var mag=ha(-0.833,true);
 return {Fajr:ha(-FAJRA,false),Sunrise:ha(-0.833,false),Dhuhr:mid,Asr:ha(asrAlt,true),
         Maghrib:mag,Isha:ISHAMIN?mag+ISHAMIN/60:ha(-17,true)};
}
var NAMES=[['Fajr','F'],['Dhuhr','D'],['Asr','A'],['Maghrib','M'],['Isha','I']];
function fmt(h){if(!isFinite(h))return '—';h=((h%24)+24)%24;var m=Math.round(h*60)%1440;return String(Math.floor(m/60)).padStart(2,'0')+':'+String(m%60).padStart(2,'0')}
function draw(){
 var now=new Date(),t=times(new Date(now.getFullYear(),now.getMonth(),now.getDate()));
 var mins=now.getHours()*60+now.getMinutes()+now.getSeconds()/60;
 var seq=NAMES.map(function(n){return [n[0],n[1],t[n[0]]*60]});
 var next=null;for(var i=0;i<seq.length;i++)if(seq[i][2]>mins){next=seq[i];break}
 if(!next){next=seq[0];next[2]+=1440}
 var wait=next[2]-mins;
 document.getElementById('nm').textContent=next[0];
 document.getElementById('tm').textContent=fmt(next[2]/60);
 document.getElementById('in').textContent='in '+(wait>=60?Math.floor(wait/60)+'h '+Math.round(wait%60)+'m':Math.round(wait)+'m');
 document.getElementById('all').innerHTML=seq.map(function(s){return '<div><b>'+s[1]+'</b> <span>'+fmt(s[2]/60)+'</span></div>'}).join('');
 var prev=0;for(var j=0;j<seq.length;j++){var v=seq[j][2];if(v<=mins)prev=v;else{var span=v-prev;document.getElementById('fill').style.width=(span>0?Math.max(0,Math.min(100,(mins-prev)/span*100)):0)+'%';break}}
}
draw();setInterval(draw,30000);
</script>""".replace("@@LAT@@", str(LAT)).replace("@@LNG@@", str(LNG)).replace("@@TZ@@", str(TZ)).replace("@@FAJRA@@", str(FAJR_ANGLE)).replace("@@ISHAMIN@@", str(ISHA_MIN))

with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

home = [p for p in cfg["pages"] if p["id"] == "home"][0]
widgets = home["widgets"]
widgets[:] = [w for w in widgets if w.get("id") not in ("stat-4", "prayer")]
prayer = {"id": "prayer", "type": "html", "x": 9, "y": 4, "w": 3, "h": 2,
          "options": {"html": JS, "transparent": True},
          "appearance": {"style": "borderless", "radius": 0, "padding": 4, "border": False, "shadow": False}}
widgets.append(prayer)

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("PUT:", r.status)
print("home:", [(w["id"], w["x"], w["y"], w["w"], w["h"]) for w in widgets])
