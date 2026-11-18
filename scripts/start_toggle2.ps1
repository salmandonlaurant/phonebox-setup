Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$root = [System.Windows.Automation.AutomationElement]::RootElement
$cond = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::AutomationIdProperty, "StartButton")
$btn = $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $cond)
Write-Output "btn: $([bool]$btn)"
try {
    $pat = $btn.GetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern)
    Write-Output "toggle pattern OK, state=$($pat.Current.ToggleState)"
    $pat.Toggle()
    Write-Output "toggled"
} catch { Write-Output "toggle error: $($_.Exception.Message)" }
Start-Sleep -Milliseconds 1200
$walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
$c = $walker.GetFirstChild($root)
while ($c) {
    Write-Output ("TOP: '$($c.Current.Name)' | cls=$($c.Current.ClassName)")
    $c = $walker.GetNextSibling($c)
}
