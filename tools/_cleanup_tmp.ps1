$paths = @(
  "C:\Users\neura\repos\audio-device-switcher\assets\advanced-verify.png",
  "C:\Users\neura\repos\audio-device-switcher\assets\advanced-crop.png",
  "C:\Users\neura\repos\audio-device-switcher\tools\_reset_adv.ps1"
)
foreach ($path in $paths) {
  if (Test-Path -LiteralPath $path) {
    Remove-Item -LiteralPath $path -Force
    Write-Output ("removed " + $path)
  } else {
    Write-Output ("missing " + $path)
  }
}
