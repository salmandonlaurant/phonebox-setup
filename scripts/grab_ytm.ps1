Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;using System.Runtime.InteropServices;
public class W {
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int n);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
 [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L,T,R,B; }
}
"@
$procs = Get-Process brave -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -eq 'YouTube Music' }
if (-not $procs) { Write-Output 'NO_YTM_WINDOW'; exit 1 }
$hwnd = $procs[0].MainWindowHandle
[void][W]::ShowWindow($hwnd, 9)
[void][W]::SetForegroundWindow($hwnd)
Start-Sleep -Milliseconds 800
[System.Windows.Forms.SendKeys]::SendWait('^a')
Start-Sleep -Milliseconds 400
[System.Windows.Forms.SendKeys]::SendWait('^c')
Start-Sleep -Milliseconds 1200
try { $html = [System.Windows.Forms.Clipboard]::GetText([System.Windows.Forms.TextDataFormat]::Html) } catch { $html = '' }
$text = Get-Clipboard -Format Text -Raw -ErrorAction SilentlyContinue
[System.IO.File]::WriteAllText("$env:TEMP\phonebox-ytm-clip.html", [string]$html, [System.Text.Encoding]::UTF8)
[System.IO.File]::WriteAllText("$env:TEMP\phonebox-ytm-clip.txt", [string]$text, [System.Text.Encoding]::UTF8)
Write-Output "HTML_LEN: $($html.Length)"
Write-Output "TEXT_LEN: $($text.Length)"
$s = [string]$text
$preview = if ($s.Length -gt 600) { $s.Substring(0,600) } else { $s }
Write-Output "TEXT_PREVIEW: $preview"
