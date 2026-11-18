$exe = "C:\Users\Admin\AppData\Local\PhoneBox\app\PhoneBoxAgent.exe"
$start = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
$lnk  = Join-Path $start "PhoneBox.lnk"
$sh = New-Object -ComObject WScript.Shell
$s = $sh.CreateShortcut($lnk)
$s.TargetPath = $exe
$s.WorkingDirectory = (Split-Path $exe)
$s.Description = "PhoneBox desk panel agent"
$s.IconLocation = "$exe,0"
$s.Save()
Write-Output "created: $lnk exists=$(Test-Path $lnk)"
