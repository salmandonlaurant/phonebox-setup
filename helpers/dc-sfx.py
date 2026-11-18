import json, os, struct, uuid, time, sys

TOKEN_PATH = os.path.join(os.environ["APPDATA"], "PhoneBox", "discord-token.json")
CLIENT_ID = "1572354807363149834"

def frame(op, obj):
    b = json.dumps(obj, separators=(",", ":")).encode("utf-8")
    return struct.pack("<II", op, len(b)) + b

def rx(f, n):
    out = b""
    while len(out) < n:
        c = f.read(n - len(out))
        if not c:
            raise EOFError
        out += c
    return out

def rf(f):
    op, ln = struct.unpack("<II", rx(f, 8))
    return op, (json.loads(rx(f, ln).decode("utf-8")) if ln else None)

def call(f, cmd, args, wait=5):
    nonce = uuid.uuid4().hex
    f.write(frame(1, {"cmd": cmd, "nonce": nonce, "args": args}))
    f.flush()
    end = time.time() + wait
    while time.time() < end:
        op, m = rf(f)
        if not m or m.get("nonce") != nonce:
            continue
        if m.get("evt") == "ERROR":
            return False, (m.get("data") or {}).get("message", "error")
        return True, m.get("data")
    return False, "timeout"

def main():
    if len(sys.argv) < 3:
        return
    sound_id = sys.argv[1]
    guild_id = sys.argv[2]
    token = json.load(open(TOKEN_PATH, encoding="utf-8"))
    f = None
    for i in range(10):
        try:
            f = open(r"\\.\pipe\discord-ipc-%d" % i, "r+b", buffering=0)
            break
        except OSError:
            pass
    if f is None:
        return
    try:
        f.write(frame(0, {"v": 1, "client_id": CLIENT_ID}))
        f.flush()
        rf(f)
        call(f, "AUTHENTICATE", {"access_token": token["Access"]})
        args = {"sound_id": sound_id}
        if guild_id and guild_id != "0":
            args["guild_id"] = guild_id
        call(f, "PLAY_SOUNDBOARD_SOUND", args)
    finally:
        f.close()

if __name__ == "__main__":
    main()
