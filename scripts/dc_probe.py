import json, os, struct, uuid, sys

TOKEN_PATH = os.path.join(os.environ["APPDATA"], "PhoneBox", "discord-token.json")
CLIENT_ID = "1572354807363149834"

def frame(op, obj):
    b = json.dumps(obj, separators=(",", ":")).encode("utf-8")
    return struct.pack("<II", op, len(b)) + b

def read_exact(f, n):
    out = b""
    while len(out) < n:
        chunk = f.read(n - len(out))
        if not chunk:
            raise EOFError("pipe closed")
        out += chunk
    return out

def read_frame(f):
    head = read_exact(f, 8)
    op, ln = struct.unpack("<II", head)
    body = read_exact(f, ln) if ln else b""
    return op, (json.loads(body.decode("utf-8")) if body else None)

def call(f, cmd, args=None, wait=5.0):
    nonce = uuid.uuid4().hex
    f.write(frame(1, {"cmd": cmd, "nonce": nonce, "args": args or {}}))
    f.flush()
    import time
    end = time.time() + wait
    while time.time() < end:
        op, msg = read_frame(f)
        if not msg or msg.get("nonce") != nonce:
            continue
        if msg.get("evt") == "ERROR":
            return False, (msg.get("data") or {}).get("message", "error")
        return True, msg.get("data")
    return False, "timeout"

tok = json.load(open(TOKEN_PATH, encoding="utf-8"))
print("token client id matches:", tok.get("ClientId") == CLIENT_ID)
print("has access token:", bool(tok.get("Access")))

f = None
for i in range(10):
    try:
        f = open(r"\\.\pipe\discord-ipc-%d" % i, "r+b", buffering=0)
        print("connected to pipe", i)
        break
    except OSError:
        pass
if f is None:
    print("no discord pipe")
    sys.exit(1)

try:
    f.write(frame(0, {"v": 1, "client_id": CLIENT_ID}))
    f.flush()
    op, ready = read_frame(f)
    print("handshake evt:", (ready or {}).get("evt"))

    ok, data = call(f, "AUTHENTICATE", {"access_token": tok["Access"]})
    print("AUTHENTICATE:", ok, (data or {}).get("user", {}).get("username") if isinstance(data, dict) else data)

    for cmd in ["GET_SOUNDBOARD_SOUNDS", "GET_RELATIONSHIPS", "GET_GUILDS"]:
        ok, data = call(f, cmd, {})
        if ok:
            if isinstance(data, dict):
                for k, v in data.items():
                    print(cmd, "OK", k, "count=", len(v) if isinstance(v, list) else type(v).__name__)
            else:
                print(cmd, "OK", type(data).__name__)
        else:
            print(cmd, "FAIL", data)
finally:
    f.close()
