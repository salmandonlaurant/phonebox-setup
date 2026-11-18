import json
d = json.load(open(r"C:\Users\Admin\AppData\Local\Temp\opencode\pair.json", encoding="utf-8"))
qr = d["qr"]
html = """<!doctype html>
<html><head><meta charset="utf-8"><title>PhoneBox - Pair tablet</title>
<style>
  body{margin:0;min-height:100vh;background:#000;color:#fff;font-family:"Segoe UI",system-ui,sans-serif;
       display:flex;align-items:center;justify-content:center}
  .box{text-align:center;padding:28px 40px;max-width:760px}
  h1{font-size:30px;margin:0 0 6px;color:#0A84FF}
  p{font-size:17px;color:#c9d1d9;margin:8px 0}
  .qr{background:#fff;padding:18px;border-radius:20px;display:inline-block;margin:14px 0;box-shadow:0 10px 40px rgba(0,140,255,.25)}
  .qr svg{width:440px;height:440px;display:block}
  .code{font-size:34px;font-weight:700;letter-spacing:3px;color:#0A84FF;margin:10px 0}
  .steps{text-align:left;display:inline-block;font-size:17px;line-height:1.7;color:#e6e6e6;margin-top:6px}
  .small{font-size:14px;color:#888}
</style></head><body>
<div class="box">
  <h1>Pair your MODIO M19</h1>
  <p>Scan this QR code with the <b>tablet's camera</b> (not the PC).</p>
  <div class="qr">__QR__</div>
  <p>Then tap <b>Open in PhoneBox</b> and confirm this code on the tablet:</p>
  <div class="code">__CHECK__</div>
  <div class="steps">
    1. Open the tablet's Camera app and point it at the QR above.<br>
    2. Tap the link / <b>Open in PhoneBox</b>.<br>
    3. Check the code matches <b>__CHECK__</b>, then tap <b>Pair</b>.<br>
    4. The tablet will reconnect to <b>__HOST__:__PORT__</b>.
  </div>
  <p class="small">Single use - expires in 5 minutes.</p>
</div>
</body></html>""".replace("__QR__", qr).replace("__CHECK__", d["check"]).replace("__HOST__", d["hosts"][0]).replace("__PORT__", str(d["port"]))
out = r"C:\Users\Admin\AppData\Local\Temp\opencode\pair.html"
open(out, "w", encoding="utf-8").write(html)
print(out, len(html))
