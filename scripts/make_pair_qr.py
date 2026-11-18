import json, urllib.request, html, datetime

BASE = "http://127.0.0.1:8765"
req = urllib.request.Request(BASE + "/api/pair/start", data=b"", method="POST")
with urllib.request.urlopen(req, timeout=20) as r:
    d = json.loads(r.read().decode())

print("enabled:", d.get("enabled"), "| pc:", d.get("pc"))
print("hosts:", d.get("hosts"), "| port:", d.get("port"))
print("attempt:", d.get("attempt"), "claims:", d.get("claims"))
print("expires in:", round((d["expiresAt"]/1000 - __import__('time').time()), 1), "s")
print("link:", d.get("link"))
print("app:", d.get("app"))

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>PhoneBox - New Phone Setup</title>
<style>
 body{background:#000;color:#eee;font-family:Segoe UI,Roboto,sans-serif;margin:0;padding:24px;text-align:center}
 h1{font-size:22px;margin:0 0 4px}
 p.sub{color:#999;font-size:13px;margin:0 0 22px}
 .row{display:flex;gap:28px;justify-content:center;flex-wrap:wrap}
 .card{background:#141418;border:1px solid #2b2b33;border-radius:20px;padding:18px;width:330px;box-shadow:0 8px 30px rgba(0,0,0,.5)}
 .card h2{font-size:15px;margin:0 0 10px;color:#fff}
 .card .qr{background:#fff;border-radius:12px;padding:10px;display:inline-block}
 .card .qr svg{width:220px;height:220px;display:block}
 .card p{font-size:12px;color:#aaa;line-height:1.5;margin:12px 0 0}
 .num{display:inline-block;background:#ff0033;color:#fff;width:22px;height:22px;border-radius:50%;line-height:22px;font-size:12px;margin-right:6px}
 .foot{margin-top:22px;font-size:12px;color:#888}
</style></head><body>
<h1>PhoneBox - Set up your other phone</h1>
<p class="sub">Scan with the phone you want to use instead of the tablet.</p>
<div class="row">
 <div class="card"><h2><span class="num">1</span>Install the app</h2>
  <div class="qr">@@APPQR@@</div>
  <p>Opens the PhoneBox APK download on your phone. Allow install from this source, then open PhoneBox.</p>
 </div>
 <div class="card"><h2><span class="num">2</span>Pair with this PC</h2>
  <div class="qr">@@QR@@</div>
  <p>In PhoneBox, choose <b>Pair / Add PC</b> and scan this code. Make sure the phone is on the same Wi-Fi as this PC.</p>
 </div>
</div>
<p class="foot">PC: @@PC@@ &nbsp;|&nbsp; @@HOSTS@@:@@PORT@@ &nbsp;|&nbsp; Pairing attempt @@ATTEMPT@@ &nbsp;|&nbsp; @@EXP@@</p>
</body></html>"""

exp = ("Expires " + datetime.datetime.fromtimestamp(d["expiresAt"]/1000).strftime("%H:%M:%S")) if d.get("expiresAt") else ""
out = (PAGE.replace("@@APPQR@@", d.get("appQr") or "")
          .replace("@@QR@@", d.get("qr") or "")
          .replace("@@PC@@", html.escape(str(d.get("pc"))))
          .replace("@@HOSTS@@", html.escape(", ".join(d.get("hosts") or [])))
          .replace("@@PORT@@", str(d.get("port")))
          .replace("@@ATTEMPT@@", str(d.get("attempt")))
          .replace("@@EXP@@", html.escape(exp)))

path = r"C:\Users\Admin\AppData\Local\Temp\opencode\phonebox-pair-qr.html"
with open(path, "w", encoding="utf-8") as f:
    f.write(out)
print("HTML:", path)
