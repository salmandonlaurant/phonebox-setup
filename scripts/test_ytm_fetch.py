import yt_dlp

url = "https://music.youtube.com/playlist?list=LM"
opts = {
    "cookiesfrombrowser": ("brave",),
    "extract_flat": True,
    "skip_download": True,
    "quiet": True,
    "no_warnings": False,
    "playlistend": 10,
}
try:
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    print("TITLE:", info.get("title"))
    print("ID:", info.get("id"))
    entries = info.get("entries") or []
    print("COUNT:", len(entries))
    for e in entries[:10]:
        print(" -", e.get("id"), "|", e.get("title"))
except Exception as ex:
    print("ERROR:", type(ex).__name__, str(ex)[:800])
