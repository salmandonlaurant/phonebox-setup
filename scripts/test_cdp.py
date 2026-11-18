import subprocess, time, json, urllib.request

BRAVE = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
args = [BRAVE, "--remote-debugging-port=9222", "--remote-allow-origins=*",
        "--no-first-run", "--no-default-browser-check"]
p = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("launched pid", p.pid)
for i in range(20):
    time.sleep(0.5)
    try:
        with urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=2) as r:
            d = json.loads(r.read().decode())
            print("CDP_OK", d.get("Browser"), d.get("webSocketDebuggerUrl"))
            print("KEEP_RUNNING")
            raise SystemExit(0)
    except Exception:
        pass
print("CDP_FAILED")
