param(
  [Parameter(Mandatory = $true)][string]$VideoId
)

$ErrorActionPreference = 'SilentlyContinue'

# Only real 11-character YouTube ids are allowed.
if ($VideoId -notmatch '^[A-Za-z0-9_-]{11}$') { exit 1 }

Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Threading;

public static class YtmWindow {
  delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc p, IntPtr l);
  [DllImport("user32.dll")] static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] static extern bool PostMessage(IntPtr h, uint msg, IntPtr w, IntPtr l);
  [DllImport("user32.dll", CharSet = CharSet.Auto)] static extern IntPtr SendMessageTimeout(IntPtr h, uint msg, IntPtr w, IntPtr l, uint flags, uint timeout, out IntPtr result);
  [DllImport("user32.dll", EntryPoint = "GetWindowLongPtrW")] static extern IntPtr GetWindowLongPtr(IntPtr h, int idx);
  [DllImport("user32.dll", EntryPoint = "SetWindowLongPtrW")] static extern IntPtr SetWindowLongPtr(IntPtr h, int idx, IntPtr val);
  [DllImport("user32.dll")] static extern bool SetLayeredWindowAttributes(IntPtr h, uint cr, byte alpha, uint flags);

  const uint WM_CLOSE = 0x0010;
  const uint WM_SYSCOMMAND = 0x0112;
  const uint SC_CLOSE = 0xF060;
  const uint SMTO_ABORTIFHUNG = 0x0002;

  static readonly HashSet<IntPtr> Existing = new HashSet<IntPtr>();
  static readonly Dictionary<uint, string> Names = new Dictionary<uint, string>();
  static volatile bool watching = false;
  static Thread watcher;

  static string ProcName(uint pid) {
    string name;
    if (Names.TryGetValue(pid, out name)) return name;
    try { name = System.Diagnostics.Process.GetProcessById((int)pid).ProcessName; }
    catch { name = ""; }
    Names[pid] = name;
    return name;
  }

  static bool IsMusic(IntPtr h) {
    uint p; GetWindowThreadProcessId(h, out p);
    if (ProcName(p) != "brave") return false;
    var sb = new StringBuilder(512);
    GetWindowText(h, sb, 512);
    return sb.ToString().IndexOf("YouTube Music", StringComparison.OrdinalIgnoreCase) >= 0;
  }

  // Ask every existing YouTube Music window to close, politely then firmly.
  public static void CloseOld() {
    EnumWindows((h, l) => {
      if (IsMusic(h)) {
        PostMessage(h, WM_SYSCOMMAND, new IntPtr(SC_CLOSE), IntPtr.Zero);
        IntPtr r;
        SendMessageTimeout(h, WM_CLOSE, IntPtr.Zero, IntPtr.Zero, SMTO_ABORTIFHUNG, 1500, out r);
      }
      return true;
    }, IntPtr.Zero);
  }

  public static int Count() {
    int n = 0;
    EnumWindows((h, l) => { if (IsMusic(h)) n++; return true; }, IntPtr.Zero);
    return n;
  }

  public static void WatchStart() {
    Existing.Clear();
    EnumWindows((h, l) => { uint p; GetWindowThreadProcessId(h, out p); if (ProcName(p) == "brave") Existing.Add(h); return true; }, IntPtr.Zero);
    watching = true;
    watcher = new Thread(WatchLoop);
    watcher.IsBackground = true;
    watcher.Start();
  }

  public static void WatchStop() {
    watching = false;
    if (watcher != null) watcher.Join(1000);
  }

  static void WatchLoop() {
    while (watching) {
      EnumWindows((h, l) => {
        if (Existing.Contains(h)) return true;
        uint p; GetWindowThreadProcessId(h, out p);
        if (ProcName(p) == "brave") {
          var sb = new StringBuilder(512);
          GetWindowText(h, sb, 512);
          if (sb.Length > 0) {
            IntPtr ex = GetWindowLongPtr(h, -20);
            SetWindowLongPtr(h, -20, new IntPtr(ex.ToInt64() | 0x00080000L));
            SetLayeredWindowAttributes(h, 0, 0, 0x2);
          }
        }
        return true;
      }, IntPtr.Zero);
      Thread.Sleep(5);
    }
  }
}
"@

$base  = 'C:\Users\Admin\AppData\Local\PhoneBox'
$latest = Join-Path $base 'ytm-latest.txt'
$played = Join-Path $base 'ytm-played.txt'

# Record this tap as the newest request before waiting on the lock, so a burst of
# taps collapses to one launch of the last song instead of playing each in turn.
[System.IO.File]::WriteAllText($latest, $VideoId)

$mutex = New-Object System.Threading.Mutex($false, 'Global\PhoneBoxYtmLaunch')
$owned = $false
try {
  try { $owned = $mutex.WaitOne(20000) }
  catch [System.Threading.AbandonedMutexException] { $owned = $true }
  if (-not $owned) { exit 0 }

  # Play only the newest requested song; queued helpers for older taps drop out.
  $target = ([System.IO.File]::ReadAllText($latest)).Trim()
  if ($target -notmatch '^[A-Za-z0-9_-]{11}$') { $target = $VideoId }
  $last = ''
  if (Test-Path $played) { $last = ([System.IO.File]::ReadAllText($played)).Trim() }
  if ($target -eq $last -and [YtmWindow]::Count() -gt 0) { exit 0 }

  # Close the previous song and wait for its window to actually disappear.
  # Only start the new one once no old YouTube Music window remains.
  for ($round = 0; $round -lt 3 -and [YtmWindow]::Count() -gt 0; $round++) {
    [YtmWindow]::CloseOld()
    for ($i = 0; $i -lt 50 -and [YtmWindow]::Count() -gt 0; $i++) {
      Start-Sleep -Milliseconds 150
    }
  }
  if ([YtmWindow]::Count() -gt 0) {
    # Never launch a second stream while an old one is still alive.
    exit 0
  }

  [YtmWindow]::WatchStart()
  $brave = 'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
  Start-Process -FilePath $brave -ArgumentList @("--app=https://music.youtube.com/watch?v=$target")
  Start-Sleep -Milliseconds 2500
  [YtmWindow]::WatchStop()
  [System.IO.File]::WriteAllText($played, $target)
}
finally {
  if ($owned) { $mutex.ReleaseMutex() }
  $mutex.Dispose()
}
