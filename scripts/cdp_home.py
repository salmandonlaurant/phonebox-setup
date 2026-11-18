import json, urllib.request, time
import websocket

with urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=5) as r:
    targets = json.loads(r.read().decode())
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

cmd("Page.navigate", {"url": "https://music.youtube.com/"})
time.sleep(10)
for i in range(15):
    js("window.scrollTo(0, document.body.scrollHeight); true")
    time.sleep(0.5)

print("TITLE:", js("document.title"))
print("LOGGED_IN:", js("typeof ytcfg !== 'undefined' ? ytcfg.get('LOGGED_IN') : 'no-ytcfg'"))
print("ACCOUNT_NAME:", js("typeof ytcfg !== 'undefined' ? ytcfg.get('ACCOUNT_NAME') : null"))
print("CHANNEL_ID:", js("typeof ytcfg !== 'undefined' ? ytcfg.get('CHANNEL_ID') : null"))
print("GUIDE_TEXT:", repr((js("document.body.innerText") or "")[:800]))
print("WATCH_ANCHORS:", js("document.querySelectorAll('a[href*=\"watch?v=\"]').length"))
print("SAMPLE:", js("Array.from(document.querySelectorAll('a[href*=\"watch?v=\"]')).slice(0,20).map(a=>({h:a.getAttribute('href'),t:(a.innerText||a.getAttribute('aria-label')||'').trim().slice(0,70)}))"))
ws.close()
