# Rebuilds the exact ATtiny1616 image. Install Arduino CLI and
# megaTinyCore:megaavr 2.6.11 first; see README.md.
$projectDir = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$localCli = Join-Path $projectDir 'tools\arduino-cli\arduino-cli.exe'
$buildDir = Join-Path $projectDir 'tools\arduino-cli\build'
$sketchDir = Join-Path $PSScriptRoot 'WaterEarring'
$hexFile = Join-Path $PSScriptRoot 'WaterEarring_ATtiny1616_16MHz.hex'
$fqbn = 'megaTinyCore:megaavr:atxy6:chip=1616,clock=16internal,millis=enabled,startuptime=8,bodvoltage=2v6,bodmode=enabled,eesave=enable,resetpin=UPDI,printf=default,wiremode=mors,WDTtimeout=disabled,WDTwindow=disabled,PWMmux=A_default,attach=allenabled'

if (Test-Path -LiteralPath $localCli) {
    $cli = $localCli
    $cliArgs = @('--config-dir', (Join-Path $projectDir 'tools\arduino-cli\data'))
} else {
    $command = Get-Command arduino-cli -ErrorAction SilentlyContinue
    if (-not $command) { throw 'Arduino CLI was not found. Install it and megaTinyCore before building.' }
    $cli = $command.Source
    $cliArgs = @()
}

New-Item -ItemType Directory -Force -Path $buildDir | Out-Null
& $cli @cliArgs compile --build-path $buildDir --fqbn $fqbn $sketchDir
if ($LASTEXITCODE -ne 0) { throw 'Firmware compilation failed.' }
Copy-Item -LiteralPath (Join-Path $buildDir 'WaterEarring.ino.hex') -Destination $hexFile -Force
Get-FileHash -LiteralPath $hexFile -Algorithm SHA256 | Select-Object Path, Hash
