Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$root = [System.Windows.Automation.AutomationElement]::RootElement
$cond = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::AutomationIdProperty, "StartButton")
$btn = $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $cond)
foreach ($p in @([System.Windows.Automation.TogglePattern]::Pattern,
                 [System.Windows.Automation.SelectionItemPattern]::Pattern,
                 [System.Windows.Automation.LegacyIAccessiblePattern]::Pattern)) {
    try {
        $pat = $btn.GetCurrentPattern($p)
        Write-Output "PATTERN OK: $($p.ProgrammaticName)"
        if ($pat -is [System.Windows.Automation.TogglePattern]) { $pat.Toggle(); Write-Output "toggled" }
        if ($pat -is [System.Windows.Automation.LegacyIAccessiblePattern]) { $pat.DoDefaultAction(); Write-Output "default action" }
        break
    } catch { Write-Output "no $($p.ProgrammaticName): $($_.Exception.Message.Split([char]10)[0])" }
}
Start-Sleep -Milliseconds 1000
$walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
$c = $walker.GetFirstChild($root)
while ($c) {
    Write-Output ("TOP: '$($c.Current.Name)' | cls=$($c.Current.ClassName)")
    $c = $walker.GetNextSibling($c)
}
