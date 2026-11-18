Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms

$root = [System.Windows.Automation.AutomationElement]::RootElement
$cond = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::AutomationIdProperty, "StartButton")
$startBtn = $root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $cond)
if ($startBtn) {
    try { $startBtn.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke() } catch {}
}
Start-Sleep -Milliseconds 700
[System.Windows.Forms.SendKeys]::SendWait("PhoneBox")
Start-Sleep -Milliseconds 1200

$walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
function Walk($el, $depth) {
    if ($depth -gt 6) { return }
    $c = $walker.GetFirstChild($el)
    while ($c) {
        $name = $c.Current.Name
        $type = $c.Current.ControlType.ProgrammaticName
        $aid  = $c.Current.AutomationId
        if ($name -match 'PhoneBox|Pin|taskbar|Start' -or $aid -match 'PhoneBox|Search') {
            Write-Output ((" " * ($depth * 2)) + "$type | name='$name' | aid='$aid'")
        }
        Walk $c ($depth + 1)
        $c = $walker.GetNextSibling($c)
    }
}
Walk $root 0
Write-Output "--- done ---"
