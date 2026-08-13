$ErrorActionPreference = 'Stop'
$msix = 'C:\Users\neura\.nuget\packages\microsoft.windowsappsdk.runtime\2.3.1\tools\MSIX\win10-x64\Microsoft.WindowsAppRuntime.2.msix'
$dest = Join-Path $env:TEMP 'wasdk-runtime-2.3.1'
if (Test-Path -LiteralPath $dest) { Remove-Item -LiteralPath $dest -Recurse -Force }
New-Item -ItemType Directory -Path $dest | Out-Null
$zip = Join-Path $dest 'runtime.zip'
Copy-Item -LiteralPath $msix -Destination $zip
$extracted = Join-Path $dest 'extracted'
Expand-Archive -LiteralPath $zip -DestinationPath $extracted -Force
Get-ChildItem -LiteralPath $extracted -Recurse -Filter '*Insights*' | ForEach-Object { $_.FullName + '|' + $_.Length }
Write-Output '---TOP---'
Get-ChildItem -LiteralPath $extracted | ForEach-Object { $_.Name }
