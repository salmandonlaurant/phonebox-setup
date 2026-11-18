Option Explicit
' Hidden wrapper: arg0 = agent API path (e.g. "api/media/next" or "seekrel:-10000")
Dim path, py, cmd, sh
If WScript.Arguments.Count < 1 Then WScript.Quit 1
path = WScript.Arguments(0)
py = "C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"
cmd = """" & py & """ ""C:\Users\Admin\AppData\Local\PhoneBox\agent-post.py"" " & path
Set sh = CreateObject("WScript.Shell")
sh.Run cmd, 0, False
Set sh = Nothing
