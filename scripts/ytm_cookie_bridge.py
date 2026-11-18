"""Shared helper: make yt-dlp read Brave cookies even while Brave is running."""
import os, shutil, tempfile
import yt_dlp.cookies as ck

BRAVE = os.path.join(os.environ["LOCALAPPDATA"], "BraveSoftware", "Brave-Browser", "User Data")
DB = os.path.join(BRAVE, "Default", "Network", "Cookies")
_COPY = os.path.join(tempfile.gettempdir(), "phonebox-brave-cookies.db")

def prepare():
    shutil.copyfile(DB, _COPY)
    real = ck._open_database_copy
    def patched(database_path, tmpdir):
        return real(_COPY, tmpdir)
    ck._open_database_copy = patched
    return _COPY
