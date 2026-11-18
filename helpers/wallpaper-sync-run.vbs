Option Explicit
Dim cmd, sh
cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\Users\Admin\AppData\Local\PhoneBox\wallpaper-sync.ps1"""
Set sh = CreateObject("WScript.Shell")
sh.Run cmd, 0, False
Set sh = Nothing
