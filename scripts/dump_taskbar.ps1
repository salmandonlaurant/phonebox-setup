Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

$root = [System.Windows.Automation.AutomationElement]::RootElement
$cond = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::ClassNameProperty, "Shell_TrayWnd")
$taskbar = $root.FindFirst([System.Windows.Automation.TreeScope]::Children, $cond)
if (-not $taskbar) { Write-Output "TASKBAR NOT FOUND"; exit 1 }
Write-Output "TASKBAR FOUND"
$walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
function Walk($el, $depth) {
    if ($depth -gt 4) { return }
    $c = $walker.GetFirstChild($el)
    while ($c) {
        $name = $c.Current.Name
        $type = $c.Current.ControlType.ProgrammaticName
        $cls  = $c.Current.ClassName
        $aid  = $c.Current.AutomationId
        if ($name -or $aid) {
            Write-Output ((" " * ($depth * 2)) + "$type | name='$name' | cls='$cls' | aid='$aid'")
        }
        Walk $c ($depth + 1)
        $c = $walker.GetNextSibling($c)
    }
}
Walk $taskbar 0
