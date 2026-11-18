Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;using System.Runtime.InteropServices;
public class W2 {
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int n);
}
"@
$p = Get-Process brave -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if (-not $p) { Write-Output 'NO_BRAVE'; exit 1 }
$h = $p.MainWindowHandle
[void][W2]::ShowWindow($h, 9)
[void][W2]::SetForegroundWindow($h)
Start-Sleep -Milliseconds 700

# New tab so the user's current page is preserved
[System.Windows.Forms.SendKeys]::SendWait('^t')
Start-Sleep -Milliseconds 400
[System.Windows.Forms.SendKeys]::SendWait('https://music.youtube.com/playlist?list=LM')
[System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
Start-Sleep -Seconds 7

# Scroll to load the whole list
for ($i=0; $i -lt 25; $i++) {
  [System.Windows.Forms.SendKeys]::SendWait('{END}')
  Start-Sleep -Milliseconds 450
}
Start-Sleep -Seconds 2
[System.Windows.Forms.SendKeys]::SendWait('^a')
Start-Sleep -Milliseconds 500
[System.Windows.Forms.SendKeys]::SendWait('^c')
Start-Sleep -Milliseconds 1500

try { $html = [System.Windows.Forms.Clipboard]::GetText([System.Windows.Forms.TextDataFormat]::Html) } catch { $html = '' }
$text = Get-Clipboard -Format Text -Raw -ErrorAction SilentlyContinue
[System.IO.File]::WriteAllText("$env:TEMP\phonebox-liked.html", [string]$html, [System.Text.Encoding]::UTF8)
[System.IO.File]::WriteAllText("$env:TEMP\phonebox-liked.txt", [string]$text, [System.Text.Encoding]::UTF8)
Write-Output "HTML_LEN: $($html.Length)"
Write-Output "TEXT_LEN: $($text.Length)"
$preview = if ($text.Length -gt 400) { $text.Substring(0,400) } else { [string]$text }
Write-Output "PREVIEW: $preview"

# Close the temporary tab
[System.Windows.Forms.SendKeys]::SendWait('^w')
