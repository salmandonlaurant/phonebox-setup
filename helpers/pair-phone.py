"""Generate a fresh Wi-Fi pairing QR on the PC and open it in the browser.

Triggered from the PhoneBox dashboard's Pair button (via a hidden VBS wrapper).
The phone scans the QR shown on the PC screen; nothing is sent to the phone here.
"""
import datetime
import html
import json
import urllib.request
import webbrowser

BASE = "http://127.0.0.1:8765"
OUT = r"C:\Users\Admin\AppData\Local\Temp\opencode\phonebox-pair-live.html"
LOG = r"C:\Users\Admin\AppData\Local\Temp\opencode\pair-phone-last.txt"


def main():
    try:
        req = urllib.request.Request(BASE + "/api/pair/start", data=b"", method="POST")
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        with open(LOG, "w", encoding="utf-8") as f:
            f.write("FAIL start: " + repr(e))
        return

    if not d.get("enabled"):
        with open(LOG, "w", encoding="utf-8") as f:
            f.write("FAIL: Wi-Fi pairing is disabled on the PC (turn it on in Settings and restart the agent).")
        return

    exp = ""
    if d.get("expiresAt"):
        exp = datetime.datetime.fromtimestamp(d["expiresAt"] / 1000).strftime("%H:%M:%S")

    page = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PhoneBox - Pair your phone</title>
<style>
*{box-sizing:border-box}
body{margin:0;min-height:100vh;background:#050506;color:#f2f3f7;font-family:"Segoe UI",Roboto,system-ui,sans-serif;
 display:flex;align-items:center;justify-content:center;padding:28px}
.box{width:min(720px,100%);text-align:center}
h1{font-size:30px;margin:0 0 6px;color:#fff}
.sub{color:#9da1b2;font-size:15px;margin:0 0 20px}
.qr{display:inline-block;background:#fff;border-radius:20px;padding:16px;box-shadow:0 12px 50px rgba(0,0,0,.7)}
.qr svg{width:min(360px,64vw);height:min(360px,64vw);display:block}
.steps{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin:22px 0 14px}
.step{background:#14151b;border:1px solid #2a2b34;border-radius:16px;padding:14px 18px;width:230px;text-align:left}
.step b{display:block;color:#ff5b50;font-size:13px;margin-bottom:6px;letter-spacing:.05em}
.step span{font-size:14px;color:#d5d7e0;line-height:1.45}
.foot{margin-top:14px;font-size:12px;color:#777b8c;line-height:1.7}
code{color:#c8cad6;background:#14151b;padding:2px 7px;border-radius:6px}
</style></head><body><div class="box">
<h1>Pair your phone with @@PC@@</h1>
<p class="sub">Scan this code with the PhoneBox app on your phone.</p>
<div class="qr">@@QR@@</div>
<div class="steps">
 <div class="step"><b>1 · Open PhoneBox</b><span>On the phone, open PhoneBox and choose <b>Pair / Add PC</b>, then scan the code above.</span></div>
 <div class="step"><b>2 · Same network</b><span>Phone and PC must be on the same Wi-Fi. The phone then connects automatically from now on.</span></div>
</div>
<p class="foot">PC: <code>@@PC@@</code> &nbsp;•&nbsp; Address: <code>@@HOSTS@@:@@PORT@@</code><br>
Expires at @@EXP@@ (5 minutes) &nbsp;•&nbsp; Pairing attempt @@ATTEMPT@@<br>
If it expires, tap <b>Pair Phone</b> again on the dashboard to get a fresh code.</p>
</div></body></html>"""

    out = (page.replace("@@QR@@", d.get("qr") or "")
               .replace("@@PC@@", html.escape(str(d.get("pc"))))
               .replace("@@HOSTS@@", html.escape(", ".join(d.get("hosts") or [])))
               .replace("@@PORT@@", str(d.get("port")))
               .replace("@@EXP@@", html.escape(exp))
               .replace("@@ATTEMPT@@", str(d.get("attempt"))))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)
    webbrowser.open("file:///" + OUT.replace("\\", "/"))
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("OK pc=%s hosts=%s port=%s exp=%s attempt=%s\n" %
                (d.get("pc"), ",".join(d.get("hosts") or []), d.get("port"), exp, d.get("attempt")))


if __name__ == "__main__":
    main()
