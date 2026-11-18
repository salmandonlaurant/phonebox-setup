import json, urllib.request
req = urllib.request.Request("http://127.0.0.1:8765/api/pair/start", data=b"", method="POST")
with urllib.request.urlopen(req, timeout=20) as r:
    d = json.load(r)
with open(r"C:\Users\Admin\AppData\Local\Temp\opencode\pair.json", "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("pc:", d.get("pc"))
print("hosts:", d.get("hosts"))
print("port:", d.get("port"))
print("check code:", d.get("check"))
print("expiresAt:", d.get("expiresAt"))
print("attempt:", d.get("attempt"))
print("has qr:", bool(d.get("qr")), "qr chars:", len(d.get("qr") or ""))
print("link:", d.get("link"))
