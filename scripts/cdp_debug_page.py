import json, urllib.request, time
import websocket

with urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=5) as r:
    targets = json.loads(r.read().decode())
page = next(t for t in targets if t.get("type") == "page")
print("TARGET:", page.get("url"))
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

print("TITLE:", js("document.title"))
print("URL:", js("location.href"))
print("BODYTEXT:", repr((js("document.body.innerText") or "")[:1200]))
print("ANCHORS:", js("document.querySelectorAll('a').length"))
print("WATCH_LINKS:", js("document.querySelectorAll('a[href*=\"watch\"]').length"))
print("YT_MUSIC_ITEMS:", js("document.querySelectorAll('ytmusic-responsive-list-item-renderer').length"))
print("SIGNIN:", js("document.body.innerText.includes('Sign in')"))
print("AVATAR:", js("!!document.querySelector('ytmusic-avatar-button')"))
print("HTMLSNIP:", repr((js("document.body.innerHTML") or "")[:1500]))
ws.close()
