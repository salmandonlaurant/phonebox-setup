Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$root = [System.Windows.Automation.AutomationElement]::RootElement
$cond = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::AutomationIdProperty, "StartButton")
$btn = $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $cond)
Write-Output "start button found: $([bool]$btn)"
if ($btn) {
    try {
        $btn.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
        Write-Output "invoked"
    } catch { Write-Output "invoke error: $($_.Exception.Message)" }
}
Start-Sleep -Milliseconds 1000
$walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
$c = $walker.GetFirstChild($root)
while ($c) {
    Write-Output ("TOP: '$($c.Current.Name)' | cls=$($c.Current.ClassName) | type=$($c.Current.ControlType.ProgrammaticName)")
    $c = $walker.GetNextSibling($c)
}
