#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$project = Join-Path $root 'src\AudioProfiles\AudioProfiles.csproj'
$publish = Join-Path $root 'src\AudioProfiles\bin\publish\win-x64'
$payload = Join-Path $root 'installer\payload'
$dist = Join-Path $root 'dist'
$nsis = Join-Path $root 'installer\AudioProfiles.nsi'
$makensis = 'C:\Program Files (x86)\NSIS\makensis.exe'

if (-not (Test-Path -LiteralPath $makensis)) {
    throw "NSIS was not found at $makensis"
}

New-Item -ItemType Directory -Force -Path $publish, $payload, $dist | Out-Null

dotnet publish $project -c Release -p:Platform=x64 -r win-x64 --self-contained true -o $publish --nologo
if ($LASTEXITCODE -ne 0) {
    throw "dotnet publish failed with exit code $LASTEXITCODE"
}

robocopy $publish $payload /E /NFL /NDL /NJH /NJS /nc /ns /np | Out-Null
if ($LASTEXITCODE -ge 8) {
    throw "robocopy failed with exit code $LASTEXITCODE"
}

& $makensis $nsis
if ($LASTEXITCODE -ne 0) {
    throw "makensis failed with exit code $LASTEXITCODE"
}

Write-Output (Join-Path $dist 'AudioProfilesSetup-1.0.3.exe')
