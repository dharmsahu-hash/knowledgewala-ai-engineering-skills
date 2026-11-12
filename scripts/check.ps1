# Local quality gate. Run before every commit:  powershell -File scripts/check.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$py = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }
$env:PYTHONPATH = "tooling"
& $py -m pytest -q -p no:cacheprovider; if ($LASTEXITCODE) { exit 1 }
& $py -m kw_skills validate; if ($LASTEXITCODE) { exit 1 }
& $py -m kw_skills compatibility; if ($LASTEXITCODE) { exit 1 }
& $py -m kw_skills docs --check; if ($LASTEXITCODE) { exit 1 }
Write-Host "ALL CHECKS PASSED"
