import json, urllib.request

BASE = "http://127.0.0.1:8765"
with urllib.request.urlopen(BASE + "/api/settings", timeout=15) as r:
    cfg = json.loads(r.read().decode("utf-8"))

old = "var b=L.querySelectorAll('.s');for(var j=0;j<b.length;j++)b[j].addEventListener('click',function(){var el=this;el.classList.add('hit');setTimeout(function(){el.classList.remove('hit')},300);phonebox.run(el.getAttribute('data-id'))})"
new = "var b=L.querySelectorAll('.s');for(var j=0;j<b.length;j++)b[j].addEventListener('click',function(){if(window.__ytBusy)return;window.__ytBusy=true;var el=this;el.classList.add('hit');setTimeout(function(){el.classList.remove('hit')},300);phonebox.run(el.getAttribute('data-id'));setTimeout(function(){window.__ytBusy=false},2500)})"

changed = 0
for page in cfg.get("pages", []):
    if page.get("id") != "ai":
        continue
    for w in page["widgets"]:
        if w.get("id") == "ytm-picker":
            html = w["options"].get("html", "")
            if old in html:
                w["options"]["html"] = html.replace(old, new)
                changed += 1
            elif "__ytBusy" in html:
                changed += 1

body = json.dumps(cfg, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "/api/settings", data=body, method="PUT",
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=20) as r:
    print("PUT:", r.status, "picker updated:", changed)
with urllib.request.urlopen(urllib.request.Request(BASE + "/api/refresh", data=b"", method="POST"), timeout=20) as r:
    print("refresh:", r.status)
