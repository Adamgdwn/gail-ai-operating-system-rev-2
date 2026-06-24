param(
    [int]$Port = 4173,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$host.UI.RawUI.WindowTitle = "GAIL Command Center"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$appDir = Join-Path $repoRoot "apps\command-center"
$packageJson = Join-Path $appDir "package.json"
$nodeModules = Join-Path $appDir "node_modules"
$url = "http://127.0.0.1:$Port/"

function Find-Npm {
    $npmCommand = Get-Command "npm.cmd" -ErrorAction SilentlyContinue
    if ($null -eq $npmCommand) {
        $npmCommand = Get-Command "npm" -ErrorAction SilentlyContinue
    }
    if ($null -eq $npmCommand) {
        throw "npm was not found on PATH. Install Node.js or open a terminal with npm available."
    }
    return $npmCommand.Source
}

function Test-CommandCenterServer {
    param([string]$TargetUrl)

    try {
        $response = Invoke-WebRequest -Uri $TargetUrl -UseBasicParsing -TimeoutSec 2
        return $response.Content -match "GAIL Command Center|/src/main.tsx|/assets/index"
    }
    catch {
        return $false
    }
}

function Start-BrowserWhenReady {
    param([string]$TargetUrl)

    $pollScript = @"
`$deadline = (Get-Date).AddSeconds(30)
while ((Get-Date) -lt `$deadline) {
    try {
        `$response = Invoke-WebRequest -Uri "$TargetUrl" -UseBasicParsing -TimeoutSec 2
        if (`$response.Content -match "GAIL Command Center|/src/main.tsx|/assets/index") {
            Start-Process "$TargetUrl"
            exit 0
        }
    }
    catch {
    }
    Start-Sleep -Milliseconds 500
}
Start-Process "$TargetUrl"
"@

    $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($pollScript))
    Start-Process -FilePath "powershell.exe" `
        -ArgumentList @("-NoProfile", "-WindowStyle", "Hidden", "-EncodedCommand", $encoded) `
        -WindowStyle Hidden
}

if (-not (Test-Path $packageJson)) {
    throw "Command-center package was not found at $packageJson."
}

$npm = Find-Npm

if ($DryRun) {
    Write-Host "GAIL Command Center launcher dry run"
    Write-Host "Repo: $repoRoot"
    Write-Host "App:  $appDir"
    Write-Host "URL:  $url"
    Write-Host "npm:  $npm"
    exit 0
}

if (Test-CommandCenterServer -TargetUrl $url) {
    Write-Host "GAIL Command Center is already running at $url"
    Start-Process $url
    exit 0
}

if (-not (Test-Path $nodeModules)) {
    Write-Host "Command-center dependencies are not installed."
    Write-Host "Run this from the repository root first:"
    Write-Host "  npm --prefix apps/command-center ci"
    Read-Host "Press Enter to close"
    exit 1
}

Write-Host "Starting GAIL Command Center at $url"
Write-Host "Close this window to stop the local command-center server."
Start-BrowserWhenReady -TargetUrl $url

& $npm --prefix $appDir run dev -- --port $Port --strictPort
