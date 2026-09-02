# Links this skill library into the Vault and the local Claude skills directory.
# Run from anywhere: powershell -ExecutionPolicy Bypass -File .claude\skills\install.ps1
# Re-run any time. Existing links are refreshed, real folders are left alone and reported.

$ErrorActionPreference = 'Stop'
$lib = $PSScriptRoot

$vault = 'C:\Dellcockpit home\Tyler''s Vault\08 Skills'
$claudeRoot = Join-Path $env:APPDATA 'Claude\local-agent-mode-sessions\skills-plugin'

function Link-Skill($name, $targetDir) {
    if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir | Out-Null }
    $dest = Join-Path $targetDir $name
    $src = Join-Path $lib $name
    if (Test-Path $dest) {
        $item = Get-Item $dest -Force
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            Remove-Item $dest -Force
        } else {
            Write-Host "  skip  $dest (real folder, not a link; move it aside to adopt the library copy)"
            return
        }
    }
    New-Item -ItemType Junction -Path $dest -Target $src | Out-Null
    Write-Host "  link  $dest"
}

$skills = Get-ChildItem $lib -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') }

Write-Host "Vault: $vault"
foreach ($s in $skills) { Link-Skill $s.Name $vault }

# The Claude local skills dir sits under a rotating session UUID. Find the one that already holds skills.
$claudeSkills = Get-ChildItem $claudeRoot -Directory -Recurse -Depth 3 -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -eq 'skills' } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($claudeSkills) {
    Write-Host "Claude: $($claudeSkills.FullName)"
    foreach ($s in $skills) { Link-Skill $s.Name $claudeSkills.FullName }
} else {
    Write-Host "Claude local skills directory not found under $claudeRoot. Vault links done; rerun after Claude desktop has synced once."
}

Write-Host "Done. $($skills.Count) skills linked. Restart Claude to load new ones."
