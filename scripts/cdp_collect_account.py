import json, re, time, urllib.request
import websocket

OUT = r"C:\Users\Admin\AppData\Local\Temp\phonebox-account-songs.json"

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

COLLECT = r"""
(() => {
  const out = [];
  for (const a of document.querySelectorAll('a[href*="watch?v="]')) {
    const m = (a.getAttribute('href')||'').match(/[?&]v=([A-Za-z0-9_-]{11})/);
    if (!m) continue;
    const id = m[1];
    let row = a;
    for (let i=0;i<10 && row && !row.querySelector('img');i++) row = row.parentElement;
    const txt = ((a.innerText||a.getAttribute('aria-label')||'')+'').trim();
    out.push({id, title: txt});
  }
  return out;
})()
"""

songs = {}
for url in ["https://music.youtube.com/history", "https://music.youtube.com/"]:
    cmd("Page.navigate", {"url": url})
    time.sleep(8)
    print("\nURL:", url, "| title:", js("document.title"))
    print("TEXT:", repr((js("document.body.innerText") or "")[:400]))
    for i in range(30):
        for item in (js(COLLECT) or []):
            if item["id"] not in songs and item.get("title"):
                songs[item["id"]] = item
        js("window.scrollTo(0, document.body.scrollHeight); true")
        time.sleep(0.45)
    for item in (js(COLLECT) or []):
        if item["id"] not in songs and item.get("title"):
            songs[item["id"]] = item

ws.close()
result = list(songs.values())
print("\nTOTAL:", len(result))
for s in result[:40]:
    print(" -", s["id"], "|", s["title"][:70].replace("\n", " "))
if not result:
    raise SystemExit(2)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print("SAVED:", OUT)
