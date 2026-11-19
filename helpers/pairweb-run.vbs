Option Explicit
' Hidden wrapper for the enhanced settings proxy.
Dim py, cmd, sh
py = "C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"
cmd = """" & py & """ ""C:\Users\Admin\AppData\Local\PhoneBox\pairweb.py"""
Set sh = CreateObject("WScript.Shell")
sh.Run cmd, 0, False
Set sh = Nothing
