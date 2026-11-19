Option Explicit
' Hidden wrapper: generates a fresh pairing QR and opens it on the PC screen.
Dim py, cmd, sh
py = "C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"
cmd = """" & py & """ ""C:\Users\Admin\AppData\Local\PhoneBox\pair-phone.py"""
Set sh = CreateObject("WScript.Shell")
sh.Run cmd, 0, False
Set sh = Nothing
