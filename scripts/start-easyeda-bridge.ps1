[CmdletBinding()]
param(
    [ValidateRange(1, 60)]
    [int]$StartupTimeoutSeconds = 15
)

$ErrorActionPreference = 'Stop'

$skillDirectory = 'C:\Users\hoshi\.codex\skills\easyeda-api'
$npmCommand = 'C:\Program Files\nodejs\npm.cmd'
$portRange = 49620..49629

function Get-EasyEdaBridgePort {
    foreach ($candidatePort in $portRange) {
        try {
            $health = Invoke-RestMethod -Uri "http://127.0.0.1:$candidatePort/health" -TimeoutSec 1
            if ($health.service -eq 'easyeda-bridge') {
                return [PSCustomObject]@{
                    Port   = $candidatePort
                    Health = $health
                }
            }
        }
        catch {
            # An unused port or unrelated local service is not a bridge.
        }
    }

    return $null
}

if (-not (Test-Path -LiteralPath (Join-Path $skillDirectory 'package.json'))) {
    throw "EasyEDA API skill was not found: $skillDirectory"
}
if (-not (Test-Path -LiteralPath $npmCommand)) {
    throw "npm.cmd was not found: $npmCommand"
}

$bridge = Get-EasyEdaBridgePort
if ($null -eq $bridge) {
    $tempDirectory = [System.IO.Path]::GetTempPath()
    $stdoutLog = Join-Path $tempDirectory 'easyeda-bridge.stdout.log'
    $stderrLog = Join-Path $tempDirectory 'easyeda-bridge.stderr.log'

    $process = Start-Process `
        -FilePath $npmCommand `
        -ArgumentList @('run', 'server') `
        -WorkingDirectory $skillDirectory `
        -WindowStyle Hidden `
        -RedirectStandardOutput $stdoutLog `
        -RedirectStandardError $stderrLog `
        -PassThru

    $deadline = (Get-Date).AddSeconds($StartupTimeoutSeconds)
    do {
        Start-Sleep -Milliseconds 500
        $bridge = Get-EasyEdaBridgePort
    } while ($null -eq $bridge -and (Get-Date) -lt $deadline)

    if ($null -eq $bridge) {
        $stderr = if (Test-Path -LiteralPath $stderrLog) {
            Get-Content -LiteralPath $stderrLog -Raw
        }
        else {
            ''
        }
        throw "EasyEDA Bridge did not become healthy within $StartupTimeoutSeconds seconds. Process ID: $($process.Id). Error log: $stderrLog`n$stderr"
    }

    Write-Output "EasyEDA Bridge started. Port: $($bridge.Port); launcher PID: $($process.Id)"
}
else {
    Write-Output "EasyEDA Bridge is already running. Port: $($bridge.Port)"
}

$windowResponse = Invoke-RestMethod -Uri "http://127.0.0.1:$($bridge.Port)/eda-windows" -TimeoutSec 3
if ($windowResponse.count -gt 0) {
    Write-Output "Connected EasyEDA windows: $($windowResponse.count)"
    $windowResponse.windows | ForEach-Object {
        $activeLabel = if ($_.active) { ' (active)' } else { '' }
        Write-Output "- $($_.windowId)$activeLabel"
    }
}
else {
    Write-Warning 'Bridge is ready, but no EasyEDA window is connected. Use Reconnect in the EasyEDA gateway extension.'
}
