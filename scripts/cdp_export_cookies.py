import json, time, urllib.request
import websocket

OUT = r"C:\Users\Admin\AppData\Local\Temp\phonebox-brave-cookies.txt"

# Make sure a page target exists (newer Chrome requires PUT for /json/new).
try:
    req = urllib.request.Request("http://127.0.0.1:9222/json/new?about:blank", method="PUT")
    with urllib.request.urlopen(req, timeout=10) as r:
        newpage = json.loads(r.read().decode())
    print("NEW_PAGE:", newpage.get("id"), newpage.get("url"))
except Exception as ex:
    print("NEW_PAGE_ERR:", str(ex)[:200])

time.sleep(1)
with urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=5) as r:
    targets = json.loads(r.read().decode())
print("TARGETS:", [(t.get("type"), t.get("url", "")[:60]) for t in targets])
pages = [t for t in targets if t.get("type") == "page"]
if not pages:
    print("NO_PAGE_TARGET")
    raise SystemExit(1)
ws_url = pages[0]["webSocketDebuggerUrl"]
print("WS:", ws_url)

ws = websocket.create_connection(ws_url, timeout=20, suppress_origin=True)
ws.send(json.dumps({"id": 1, "method": "Network.getAllCookies", "params": {}}))
msg = None
while True:
    msg = json.loads(ws.recv())
    if msg.get("id") == 1:
        break
ws.close()

if "error" in msg:
    print("CDP_ERROR:", msg["error"])
    raise SystemExit(1)

cookies = msg["result"]["cookies"]
print("COOKIE_COUNT:", len(cookies))

now = int(time.time())
far = now + 10 * 365 * 24 * 3600
lines = ["# Netscape HTTP Cookie File", "# Exported from Brave via CDP for PhoneBox YTM sync", ""]
for c in cookies:
    domain = c.get("domain", "")
    path = c.get("path", "/") or "/"
    secure = "TRUE" if c.get("secure") else "FALSE"
    expires = c.get("expires", -1)
    expiry = far if expires is None or expires < 0 else int(expires)
    name = c.get("name", "")
    value = c.get("value", "")
    if not name or not domain:
        continue
    flag = "TRUE" if domain.startswith(".") else "FALSE"
    lines.append("\t".join([domain, flag, path, secure, str(expiry), name, value]))

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")
print("SAVED:", OUT)
print("YT_COOKIES:", sum(1 for c in cookies if "youtube" in c.get("domain", "").lower() or "google" in c.get("domain", "").lower()))
