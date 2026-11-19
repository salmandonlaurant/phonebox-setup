# Build the small PhoneBox pairing tray app (no Visual Studio needed).
$csc = 'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe'
$src = Join-Path $PSScriptRoot '..\helpers\pairtray.cs'
$out = Join-Path $PSScriptRoot '..\helpers\PairTray.exe'
& $csc /nologo /target:winexe /out:$out /r:System.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll $src
if ($LASTEXITCODE -ne 0) { throw "csc failed with exit code $LASTEXITCODE" }
"Built $out"
