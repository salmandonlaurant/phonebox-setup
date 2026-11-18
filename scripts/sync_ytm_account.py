import json, re, sys
import yt_dlp

COOKIES = r"C:\Users\Admin\AppData\Local\Temp\phonebox-brave-cookies.txt"
OUT = r"C:\Users\Admin\AppData\Local\Temp\phonebox-account-songs.json"
URL = "https://music.youtube.com/playlist?list=LM"

opts = {
    "cookiefile": COOKIES,
    "extract_flat": True,
    "skip_download": True,
    "quiet": True,
    "no_warnings": False,
    "playlistend": 500,
    "ignoreerrors": True,
}

try:
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(URL, download=False)
except Exception as ex:
    print("FETCH_ERROR:", type(ex).__name__, str(ex)[:1200])
    sys.exit(1)

print("PLAYLIST:", info.get("title"), "| id:", info.get("id"))
entries = info.get("entries") or []
print("RAW_ENTRIES:", len(entries))

songs = []
seen = set()
for e in entries:
    if not e:
        continue
    vid = e.get("id")
    if not isinstance(vid, str) or not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
        continue
    if vid in seen:
        continue
    seen.add(vid)
    title = e.get("title") or vid
    artist = e.get("channel") or e.get("uploader") or ""
    songs.append({"id": vid, "title": title, "artist": artist})

print("VALID_SONGS:", len(songs))
for s in songs[:15]:
    print(" -", s["id"], "|", s["title"][:60], "|", s["artist"][:40])

if not songs:
    print("NO_SONGS")
    sys.exit(2)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(songs, f, ensure_ascii=False, indent=2)
print("SAVED:", OUT)
