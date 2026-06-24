param(
    [string]$ShortcutName = "GAIL Command Center"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$launcherScript = Join-Path $repoRoot "scripts\launch-command-center.ps1"
$iconPath = Join-Path $repoRoot "apps\command-center\public\gail-command-icon.ico"
$desktopPath = [Environment]::GetFolderPath("DesktopDirectory")
$shortcutPath = Join-Path $desktopPath "$ShortcutName.lnk"

if (-not (Test-Path $launcherScript)) {
    throw "Launcher script was not found at $launcherScript."
}

if (-not (Test-Path $iconPath)) {
    throw "Launcher icon was not found at $iconPath."
}

$powershell = (Get-Command "powershell.exe" -ErrorAction Stop).Source
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $powershell
$shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$launcherScript`""
$shortcut.WorkingDirectory = $repoRoot
$shortcut.IconLocation = "$iconPath,0"
$shortcut.Description = "Launch the local GAIL Command Center browser cockpit."
$shortcut.Save()

Write-Host "Installed desktop shortcut:"
Write-Host $shortcutPath
