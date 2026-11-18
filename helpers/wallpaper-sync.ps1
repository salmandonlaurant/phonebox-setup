$ErrorActionPreference = 'SilentlyContinue'

$src  = Join-Path $env:APPDATA 'Microsoft\Windows\Themes\TranscodedWallpaper'
$dest = 'C:\Users\Admin\AppData\Local\PhoneBox\wallpaper-sync\wallpaper.jpg'
$stamp = 'C:\Users\Admin\AppData\Local\PhoneBox\wallpaper-sync\last.txt'

if (-not (Test-Path $src)) { exit 0 }
New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null

$last = (Get-Item $src).LastWriteTimeUtc.Ticks.ToString()
$prev = ''
if (Test-Path $stamp) { $prev = Get-Content $stamp -Raw }

if ($last -ne $prev) {
  Copy-Item -LiteralPath $src -Destination $dest -Force
  Set-Content -LiteralPath $stamp -Value $last -NoNewline
  # Rebuild the frosted-glass panels with the new blurred wallpaper (also refreshes the tablet).
  $py = 'C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe'
  $glass = 'C:\Users\Admin\AppData\Local\PhoneBox\liquid-glass.py'
  if (Test-Path $py) { Start-Process -FilePath $py -ArgumentList "`"$glass`"" -WindowStyle Hidden -Wait }
  try {
    Invoke-RestMethod -UseBasicParsing -Method Post -Uri 'http://127.0.0.1:8765/api/refresh' -TimeoutSec 5 | Out-Null
  } catch {}
}

while ($true) { Start-Sleep -Seconds 60 }
