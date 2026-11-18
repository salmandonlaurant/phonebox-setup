import json, subprocess, time, urllib.request
import websocket

BRAVE = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
CLOSE_PS = r"C:\Users\Admin\AppData\Local\Temp\opencode\close_brave_for_sync.ps1"
OUT = r"C:\Users\Admin\AppData\Local\Temp\phonebox-account-songs.json"

def http(url, method="GET"):
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=5) as r:
        return r.read().decode()

def close_brave():
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", CLOSE_PS],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)

print("1) closing Brave...")
close_brave()

print("2) launching Brave with CDP...")
proc = subprocess.Popen([BRAVE, "--remote-debugging-port=9222", "--remote-allow-origins=*",
                         "--no-first-run", "--no-default-browser-check"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
ws_url = None
for _ in range(40):
    time.sleep(0.5)
    try:
        v = json.loads(http("http://127.0.0.1:9222/json/version"))
        ws_url = v.get("webSocketDebuggerUrl")
        if ws_url:
            break
    except Exception:
        pass
if not ws_url:
    print("CDP_FAILED")
    raise SystemExit(1)
print("   CDP ready")

# Create a page target.
try:
    p = json.loads(http("http://127.0.0.1:9222/json/new?about:blank", "PUT"))
    print("   page:", p.get("id"))
except Exception as ex:
    print("   new-page err:", str(ex)[:120])

targets = json.loads(http("http://127.0.0.1:9222/json/list"))
page = next(t for t in targets if t.get("type") == "page")
ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)

n = [0]
def cmd(method, params=None):
    n[0] += 1; mid = n[0]
    ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == mid:
            if "error" in m: raise RuntimeError(m["error"])
            return m.get("result", {})
def js(e):
    return cmd("Runtime.evaluate", {"expression": e, "returnByValue": True, "awaitPromise": True}).get("result", {}).get("value")

COLLECT = r"""
(() => {
  const out = [];
  for (const a of document.querySelectorAll('a[href*="watch?v="]')) {
    const m = (a.getAttribute('href')||'').match(/[?&]v=([A-Za-z0-9_-]{11})/);
    if (!m) continue;
    const id = m[1];
    const txt = ((a.innerText||a.getAttribute('aria-label')||'')+'').trim().replace(/\s+/g,' ');
    out.push({id, title: txt});
  }
  return out;
})()
"""

songs = {}
for url in ["https://music.youtube.com/history", "https://music.youtube.com/"]:
    print("3) scanning", url)
    cmd("Page.navigate", {"url": url})
    time.sleep(9)
    print("   page title:", js("document.title"))
    for i in range(28):
        for item in (js(COLLECT) or []):
            if item["id"] not in songs and item.get("title"):
                songs[item["id"]] = item
        js("window.scrollTo(0, document.body.scrollHeight); true")
        time.sleep(0.4)
    for item in (js(COLLECT) or []):
        if item["id"] not in songs and item.get("title"):
            songs[item["id"]] = item

ws.close()
result = list(songs.values())
print("\nTOTAL UNIQUE SONGS:", len(result))
for s in result[:60]:
    print(" -", s["id"], "|", s["title"][:70])

print("4) closing debug Brave, restoring normal Brave...")
close_brave()
time.sleep(1)
subprocess.Popen([BRAVE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if not result:
    print("NO_SONGS")
    raise SystemExit(2)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print("SAVED:", OUT)
