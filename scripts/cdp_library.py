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

for url in ["https://music.youtube.com/library/playlists", "https://music.youtube.com/library/songs"]:
    cmd("Page.navigate", {"url": url})
    time.sleep(7)
    print("\n=== ", url, " ===")
    print("TITLE:", js("document.title"))
    print("TEXT:", repr((js("document.body.innerText") or "")[:2500]))
    print("LINKS:", js("Array.from(document.querySelectorAll('a[href*=\"playlist?list=\"]')).slice(0,25).map(a=>({h:a.getAttribute('href'),t:(a.innerText||'').trim().slice(0,60)}))"))
ws.close()
