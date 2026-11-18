$bk = "C:\Users\Admin\AppData\Local\Temp\opencode\taskbar-backup"
New-Item -ItemType Directory -Path $bk -Force | Out-Null
$pinned = "$env:APPDATA\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar"
Copy-Item -Path $pinned -Destination (Join-Path $bk "PinnedTaskBar") -Recurse -Force
$layout = "$env:LOCALAPPDATA\Microsoft\Windows\Shell\LayoutModification.xml"
if (Test-Path $layout) { Copy-Item $layout (Join-Path $bk "LayoutModification.xml") -Force }
reg export "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband" (Join-Path $bk "Taskband.reg") /y | Out-Null
Write-Output "backup at $bk"
Get-ChildItem $bk -Recurse | Select-Object FullName
