# One-time fix: make the PC's LAN address stable so the phone never has to re-pair.
$ErrorActionPreference = 'Stop'
$log = 'C:\Users\Admin\AppData\Local\Temp\opencode\static-ip-result.txt'
try {
    if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw 'not elevated'
    }
    netsh interface ip set address name="Ethernet" static 192.168.1.102 255.255.255.0 192.168.1.1 1 | Out-Null
    netsh interface ip set dnsservers name="Ethernet" static 8.8.8.8 primary | Out-Null
    netsh interface ip add dnsservers name="Ethernet" 8.8.4.4 index=2 | Out-Null
    $ip = (Get-NetIPAddress -InterfaceAlias 'Ethernet' -AddressFamily IPv4).IPAddress
    $gw = (Get-NetRoute -InterfaceAlias 'Ethernet' -DestinationPrefix '0.0.0.0/0').NextHop
    "OK ip=$ip gw=$gw" | Set-Content $log -Encoding UTF8
} catch {
    "FAIL $($_.Exception.Message)" | Set-Content $log -Encoding UTF8
}
