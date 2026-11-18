$tokens = $null
$errors = $null
[System.Management.Automation.Language.Parser]::ParseFile(
    'C:\Users\Admin\AppData\Local\PhoneBox\ytm-play.ps1', [ref]$tokens, [ref]$errors) | Out-Null
if ($errors.Count) { $errors | ForEach-Object { Write-Output "ERR: $($_.Message)" } }
else { Write-Output "PowerShell syntax OK" }
