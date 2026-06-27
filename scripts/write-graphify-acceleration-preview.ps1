[CmdletBinding()]
param(
    [string]$Output,
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

if ($PrintOnly) {
    $arguments += "--print"
}

python @arguments
