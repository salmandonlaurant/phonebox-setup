import sys
sys.path.insert(0, r"C:\Users\Admin\AppData\Local\Temp\opencode")
import ytm_cookie_bridge
ytm_cookie_bridge.prepare()
import yt_dlp

for url in ["https://music.youtube.com/playlist?list=LM"]:
    opts = {
        "cookiesfrombrowser": ("brave",),
        "extract_flat": True, "skip_download": True, "quiet": True,
        "no_warnings": False, "playlistend": 15,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
        print("URL:", url)
        print("TITLE:", info.get("title"), "| ID:", info.get("id"))
        entries = info.get("entries") or []
        print("COUNT:", len(entries))
        for e in entries[:15]:
            print(" -", e.get("id"), "|", e.get("title"))
    except Exception as ex:
        print("ERROR:", type(ex).__name__, str(ex)[:1000])
