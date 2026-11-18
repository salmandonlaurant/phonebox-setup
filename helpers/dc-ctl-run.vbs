Option Explicit
' Hidden wrapper: arg0 = action (mute|deafen|leave|join), arg1 = channel id (join only)
Dim action, chan, py, cmd, sh
If WScript.Arguments.Count < 1 Then WScript.Quit 1
action = WScript.Arguments(0)
chan = ""
If WScript.Arguments.Count > 1 Then chan = WScript.Arguments(1)
py = "C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"
cmd = """" & py & """ ""C:\Users\Admin\AppData\Local\PhoneBox\dc-ctl.py"" " & action
If Len(chan) > 0 Then cmd = cmd & " " & chan
Set sh = CreateObject("WScript.Shell")
sh.Run cmd, 0, False
Set sh = Nothing
