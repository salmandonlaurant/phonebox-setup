"""Tiny local proxy for the PhoneBox settings page.

The agent's settings.html is compiled into its exe, so this serves an enhanced
copy from http://127.0.0.1:8770/ with a "Connect Device" button in the header
next to the language selector. Everything else is forwarded unchanged to the
real agent on 127.0.0.1:8765.
"""
import http.server
import socketserver
import threading
import urllib.error
import urllib.parse
import urllib.request

UPSTREAM = "127.0.0.1:8765"
PORT = 8770
DROP_HEADERS = {"origin", "referer", "sec-fetch-site", "sec-fetch-mode",
                "sec-fetch-dest", "host", "content-length", "accept-encoding"}

INJECT_CSS = """
<style>
#connectDeviceBtn{margin-left:6px;background:linear-gradient(135deg,#1f9d55,#16a34a);color:#fff;border-color:#22c55e;font-weight:600}
#connectDeviceBtn:hover{filter:brightness(1.12)}
.cd-mask{position:fixed;inset:0;background:rgba(0,0,0,.78);z-index:100;display:flex;align-items:center;justify-content:center;padding:20px}
.cd-box{background:var(--panel,#16171d);border:1px solid var(--line,#333);border-radius:18px;padding:24px;max-width:920px;width:100%;max-height:94vh;overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,.7)}
.cd-box h2{margin:0 0 4px;font-size:22px}
.cd-sub{color:var(--muted,#9aa0ae);font-size:13px;margin:0 0 18px}
.cd-cols{display:flex;gap:18px;flex-wrap:wrap}
.cd-card{flex:1 1 300px;background:rgba(255,255,255,.03);border:1px solid var(--line,#333);border-radius:14px;padding:16px}
.cd-card h3{margin:0 0 10px;font-size:15px}
.cd-qr{background:#fff;border-radius:12px;padding:10px;display:flex;align-items:center;justify-content:center;min-height:170px}
.cd-qr svg{width:190px;height:190px;display:block}
.cd-card p{color:var(--muted,#9aa0ae);font-size:12.5px;line-height:1.5;margin:10px 0 0}
.cd-foot{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:16px;font-size:12px;color:var(--muted,#9aa0ae)}
</style>
"""

INJECT_JS = """
<script>
(function(){
  function el(id){return document.getElementById(id)}
  function qrBox(svg){return '<div class="cd-qr">'+(svg||'<span style="color:#666">Unavailable</span>')+'</div>'}
  function stamp(ms){if(!ms)return '';return new Date(ms).toLocaleTimeString()}
  async function open(){
    var mask=el('cdMask');
    if(!mask){
      mask=document.createElement('div');mask.id='cdMask';mask.className='cd-mask';
      mask.innerHTML='<div class="cd-box"><h2>Connect a device</h2>'+
        '<p class="cd-sub">Scan with the PhoneBox app on the device you want to connect.</p>'+
        '<div class="cd-cols">'+
          '<div class="cd-card"><h3>1 · Pair this PC</h3><div id="cdPair">Loading…</div>'+
            '<p>In PhoneBox choose <b>Pair / Add PC</b>, then scan the left code. The device then connects over Wi-Fi automatically.</p></div>'+
          '<div class="cd-card"><h3>2 · Add another device</h3><div id="cdApp">Loading…</div>'+
            '<p>Scan the right code on a new phone or tablet to <b>download the app</b>, open it, then use the left code to pair it with this PC.</p></div>'+
        '</div>'+
        '<div class="cd-foot"><span id="cdInfo"></span><span style="flex:1"></span>'+
          '<button class="btn" id="cdRefresh">New codes</button><button class="btn primary" id="cdClose">Close</button></div>'+
      '</div>';
      document.body.appendChild(mask);
      el('cdClose').onclick=function(){mask.remove()};
      mask.addEventListener('click',function(e){if(e.target===mask)mask.remove()});
      el('cdRefresh').onclick=function(){load()};
    }
    document.body.appendChild(mask); // move to end so it stays on top
    load();
  }
  async function load(){
    el('cdPair').innerHTML='Loading…';el('cdApp').innerHTML='Loading…';el('cdInfo').textContent='';
    var r;
    try{r=await (await fetch('/api/pair/start',{method:'POST'})).json()}
    catch(e){el('cdPair').textContent='Could not reach the agent';el('cdApp').textContent='';return}
    if(!r.enabled){el('cdPair').textContent='Wi-Fi pairing is off. Turn it on in General › Wi-Fi & Tailscale, save and restart the agent.';el('cdApp').textContent='';return}
    el('cdPair').innerHTML=qrBox(r.qr);
    el('cdApp').innerHTML=qrBox(r.appQr);
    el('cdInfo').textContent='PC: '+r.pc+' · '+r.hosts.join(', ')+':'+r.port+' · expires '+stamp(r.expiresAt)+' · attempt '+r.attempt;
  }
  function boot(){
    var lang=el('langSel');if(!lang){setTimeout(boot,300);return}
    if(el('connectDeviceBtn'))return;
    var b=document.createElement('button');
    b.className='btn';b.id='connectDeviceBtn';
    b.textContent='\\uD83D\\uDCF1 Connect Device';
    b.title='Pair this PC or install PhoneBox on another device';
    b.onclick=open;
    lang.insertAdjacentElement('afterend',b);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
  // the header is rebuilt on language change, so keep re-adding the button
  setInterval(boot,1000);
})();
</script>
"""


def enhance(html_text):
    html_text = html_text.replace("</head>", INJECT_CSS + "</head>", 1)
    html_text = html_text.replace("</body>", INJECT_JS + "</body>", 1)
    return html_text


class Proxy(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    def forward(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else None
        url = "http://" + UPSTREAM + self.path
        headers = {k: v for k, v in self.headers.items() if k.lower() not in DROP_HEADERS}
        if body is not None:
            headers["Content-Length"] = str(len(body))
        req = urllib.request.Request(url, data=body, method=self.command, headers=headers)
        try:
            resp = urllib.request.urlopen(req, timeout=30)
        except urllib.error.HTTPError as e:
            resp = e
        except Exception:
            self.send_error(502, "agent offline")
            return

        data = resp.read()
        ctype = resp.headers.get("Content-Type", "application/octet-stream")
        if self.command == "GET" and self.path.split("?")[0] in ("/", ""):
            data = enhance(data.decode("utf-8", "replace")).encode("utf-8")
            ctype = "text/html; charset=utf-8"

        self.send_response(resp.status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    do_GET = forward
    do_POST = forward
    do_PUT = forward
    do_DELETE = forward
    do_HEAD = forward


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    print("PhoneBox enhanced settings on http://127.0.0.1:%d/ -> %s" % (PORT, UPSTREAM), flush=True)
    Server(("127.0.0.1", PORT), Proxy).serve_forever()
