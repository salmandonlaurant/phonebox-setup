"""Tiny hidden Discord voice-control helper.

Posts to the PhoneBox agent's own Discord RPC endpoints, so the toggle/join logic
stays in one place (the agent) and this script never flashes a console window
(it is launched through dc-ctl-run.vbs with window style 0).
"""
import json
import sys
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8765"


def main():
    if len(sys.argv) < 2:
        return
    action = sys.argv[1]
    if action not in ("mute", "deafen", "leave", "join"):
        return
    url = BASE + "/api/discord/" + action
    if action == "join" and len(sys.argv) > 2:
        url += "?channel=" + urllib.parse.quote(sys.argv[2])
    try:
        req = urllib.request.Request(url, data=b"", method="POST")
        with urllib.request.urlopen(req, timeout=8) as r:
            r.read()
    except Exception:
        pass


if __name__ == "__main__":
    main()
