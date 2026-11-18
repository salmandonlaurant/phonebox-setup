Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WinCloser {
  [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint msg, IntPtr w, IntPtr l);
}
"@

# Politely close any Brave window (WM_CLOSE).
Get-Process brave -ErrorAction SilentlyContinue |
  Where-Object { $_.MainWindowHandle -ne 0 } |
  ForEach-Object { [void][WinCloser]::PostMessage($_.MainWindowHandle, 0x0010, [IntPtr]::Zero, [IntPtr]::Zero) }

# Give it up to 10 seconds to exit on its own.
for ($i = 0; $i -lt 40; $i++) {
  Start-Sleep -Milliseconds 250
  if (-not (Get-Process brave -ErrorAction SilentlyContinue)) { break }
}

$db = Join-Path $env:LOCALAPPDATA 'BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies'
$readable = $false
try {
  $fs = [System.IO.File]::Open($db, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
  $fs.Close()
  $readable = $true
} catch { $readable = $false }

if (-not $readable) {
  # Background Brave helpers can keep the cookie DB locked; stop the remainder.
  Get-Process brave -ErrorAction SilentlyContinue | Stop-Process -Force
  Start-Sleep -Seconds 2
  try {
    $fs = [System.IO.File]::Open($db, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
    $fs.Close()
    $readable = $true
  } catch { $readable = $false }
}

$left = Get-Process brave -ErrorAction SilentlyContinue
Write-Output "BRAVE_PROCESSES: $(if ($left) { $left.Count } else { 0 })"
Write-Output "COOKIE_DB_READABLE: $readable"
