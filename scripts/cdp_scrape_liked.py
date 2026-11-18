import json, re, time, urllib.request
import websocket

OUT = r"C:\Users\Admin\AppData\Local\Temp\phonebox-account-songs.json"
URL = "https://music.youtube.com/playlist?list=LM"

with urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=5) as r:
    targets = json.loads(r.read().decode())
page = next(t for t in targets if t.get("type") == "page")
ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)

next_id = [0]
def cmd(method, params=None):
    next_id[0] += 1
    mid = next_id[0]
    ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == mid:
            if "error" in msg:
                raise RuntimeError(msg["error"])
            return msg.get("result", {})

def js(expr):
    r = cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return r.get("result", {}).get("value")

cmd("Page.enable")
cmd("Runtime.enable")
cmd("Page.navigate", {"url": URL})
print("navigated; waiting for page...")
time.sleep(10)

print("title:", js("document.title"))
print("url:", js("location.href"))

# Scroll the lazy-loading list to the bottom several times.
for i in range(25):
    js("window.scrollTo(0, document.body.scrollHeight); true")
    time.sleep(0.6)

time.sleep(2)

scrape = r"""
(() => {
  const out = [];
  const seen = new Set();
  const anchors = document.querySelectorAll('a[href*="watch?v="]');
  for (const a of anchors) {
    const m = (a.getAttribute('href') || '').match(/[?&]v=([A-Za-z0-9_-]{11})/);
    if (!m) continue;
    const id = m[1];
    if (seen.has(id)) continue;
    seen.add(id);
    let row = a;
    for (let i = 0; i < 8 && row && row.tagName !== 'YT-MUSIC-RESPONSIVE-LIST-ITEM-RENDERER'; i++) row = row.parentElement;
    let title = '';
    let artist = '';
    if (row) {
      const t = row.querySelector('.title, #title, yt-formatted-string.title');
      if (t) title = (t.innerText || t.textContent || '').trim();
      const s = row.querySelector('.secondary-text, #subscriptions, .subtitle, yt-formatted-string.secondary-text');
      if (s) artist = (s.innerText || s.textContent || '').trim();
    }
    if (!title) title = (a.innerText || a.textContent || '').trim() || id;
    out.push({id, title, artist});
  }
  return out;
})()
"""
songs = js(scrape) or []
print("SCRAPED:", len(songs))
for s in songs[:15]:
    print(" -", s["id"], "|", s["title"][:60], "|", s.get("artist", "")[:40])

ws.close()

if not songs:
    print("NO_SONGS")
    raise SystemExit(2)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(songs, f, ensure_ascii=False, indent=2)
print("SAVED:", OUT)
