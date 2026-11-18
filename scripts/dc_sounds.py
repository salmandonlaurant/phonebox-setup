import json, os, struct, uuid, time

TOKEN_PATH = os.path.join(os.environ["APPDATA"], "PhoneBox", "discord-token.json")
CLIENT_ID = "1572354807363149834"

def frame(op, obj):
    b = json.dumps(obj, separators=(",", ":")).encode()
    return struct.pack("<II", op, len(b)) + b

def rx(f, n):
    out = b""
    while len(out) < n:
        c = f.read(n - len(out))
        if not c: raise EOFError
        out += c
    return out

def rf(f):
    op, ln = struct.unpack("<II", rx(f, 8))
    return op, (json.loads(rx(f, ln).decode()) if ln else None)

def call(f, cmd, args=None, wait=6):
    nonce = uuid.uuid4().hex
    f.write(frame(1, {"cmd": cmd, "nonce": nonce, "args": args or {}})); f.flush()
    end = time.time() + wait
    while time.time() < end:
        op, m = rf(f)
        if not m or m.get("nonce") != nonce: continue
        if m.get("evt") == "ERROR": return False, (m.get("data") or {}).get("message")
        return True, m.get("data")
    return False, "timeout"

tok = json.load(open(TOKEN_PATH, encoding="utf-8"))
f = open(r"\\.\pipe\discord-ipc-0", "r+b", buffering=0)
try:
    f.write(frame(0, {"v": 1, "client_id": CLIENT_ID})); f.flush(); rf(f)
    call(f, "AUTHENTICATE", {"access_token": tok["Access"]})
    ok, data = call(f, "GET_SOUNDBOARD_SOUNDS", {})
    print("ok:", ok)
    if ok:
        sounds = data.get("soundboard_sounds", data) if isinstance(data, dict) else data
        print("count:", len(sounds))
        for s in sounds[:50]:
            print(s.get("sound_id"), "|", s.get("name"), "| guild", s.get("guild_id"), "| emoji", s.get("emoji", {}).get("name") if isinstance(s.get("emoji"), dict) else "")
        json.dump(sounds, open(os.path.join(os.environ["TEMP"], "phonebox-discord-sounds.json"), "w", encoding="utf-8"), ensure_ascii=False)
    else:
        print("error:", data)
finally:
    f.close()
