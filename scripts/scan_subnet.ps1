$ping = [System.Net.NetworkInformation.Ping]::new()
$live = @()
1..254 | ForEach-Object {
    $ip = "192.168.1.$_"
    try {
        $r = $ping.Send($ip, 250)
        if ($r.Status -eq 'Success') { $live += $ip }
    } catch {}
}
$live | Sort-Object { [int]($_.Split('.')[-1]) }
Write-Output "--- ARP cache ---"
Get-NetNeighbor -AddressFamily IPv4 -ErrorAction SilentlyContinue |
  Where-Object { $_.IPAddress -like '192.168.1.*' -and $_.State -ne 'Incomplete' } |
  Select-Object IPAddress, LinkLayerAddress, State | Format-Table -AutoSize
