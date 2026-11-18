Option Explicit
Dim sid, gid, py, cmd, sh
If WScript.Arguments.Count < 2 Then WScript.Quit 1
sid = WScript.Arguments(0)
gid = WScript.Arguments(1)
py = "C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"
cmd = """" & py & """ ""C:\Users\Admin\AppData\Local\PhoneBox\dc-sfx.py"" " & sid & " " & gid
Set sh = CreateObject("WScript.Shell")
sh.Run cmd, 0, False
Set sh = Nothing
