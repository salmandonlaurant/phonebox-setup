Option Explicit
Dim vid, cmd, sh
If WScript.Arguments.Count = 0 Then WScript.Quit 1
vid = WScript.Arguments(0)
cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File ""C:\Users\Admin\AppData\Local\PhoneBox\ytm-play.ps1"" -VideoId """ & vid & """"
Set sh = CreateObject("WScript.Shell")
sh.Run cmd, 0, False
Set sh = Nothing
