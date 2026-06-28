[CmdletBinding()]
param(
    [string]$Output,
    [string]$DiffAgainst,
    [switch]$Diff,
    [switch]$PrintOnly
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$sourceRoot = Join-Path $repoRoot "packages\uaos-core\src"

if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$sourceRoot;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $sourceRoot
}

$arguments = @(
    "-m",
    "gail_ai_operating_system.graphify_acceleration_preview",
    "--repo-root",
    $repoRoot
)

if ($Output) {
    $arguments += @("--output", $Output)
}

if ($Diff) {
    $arguments += "--diff"
}

if ($DiffAgainst) {
    $arguments += @("--diff-against", $DiffAgainst)
}

if ($PrintOnly) {
    $arguments += "--print"
}

python @arguments
