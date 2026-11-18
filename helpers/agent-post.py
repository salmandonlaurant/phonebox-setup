"""Hidden helper: POST to a PhoneBox agent endpoint.

Usage:
  agent-post.py <path>            e.g. "api/media/next"
  agent-post.py seekrel:<ms>      seek relative to the current position
"""
import json
import sys
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8765"


def main():
    if len(sys.argv) < 2:
        return
    arg = sys.argv[1].strip()

    if arg.startswith("seekrel:"):
        try:
            delta = int(arg.split(":", 1)[1])
            with urllib.request.urlopen(BASE + "/api/state", timeout=5) as r:
                state = json.loads(r.read().decode("utf-8"))
            media = state.get("media") or {}
            target = max(0, int(media.get("posMs") or 0) + delta)
            arg = "api/media/seek?ms=" + str(target)
        except Exception:
            return

    path = arg.lstrip("/")
    if not path.startswith("api/"):
        path = "api/" + path
    try:
        req = urllib.request.Request(BASE + "/" + path, data=b"", method="POST")
        with urllib.request.urlopen(req, timeout=8) as r:
            r.read()
    except Exception:
        pass


if __name__ == "__main__":
    main()
