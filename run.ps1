# Universal Runner for tool-taxonomy-arbiter (PowerShell)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$PythonCandidates = @(
    "python",
    "py -3",
    "D:\DevTools\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:ProgramFiles\Python312\python.exe",
    "$env:ProgramFiles\Python311\python.exe",
    "C:\Python312\python.exe",
    "C:\Python311\python.exe"
)

$PythonExe = $null

foreach ($cand in $PythonCandidates) {
    try {
        if ($cand -like "* *") {
            $cmd = $cand.Split(" ")[0]
            $arg = $cand.Split(" ")[1]
            & $cmd $arg --version 2>$null | Out-Null
            if ($LASTEXITCODE -eq 0) {
                $PythonExe = $cand
                break
            }
        } else {
            if (Test-Path $cand) {
                $PythonExe = $cand
                break
            }
            Get-Command $cand -ErrorAction Stop | Out-Null
            $PythonExe = $cand
            break
        }
    } catch {}
}

if (-not $PythonExe) {
    Write-Error "[ERROR] Python interpreter not found."
    exit 1
}

$ParentDir = Split-Path -Parent $ScriptDir
$env:PYTHONPATH = "$ScriptDir;$ParentDir;$env:PYTHONPATH"

if ($PythonExe -like "* *") {
    $cmd = $PythonExe.Split(" ")[0]
    $arg = $PythonExe.Split(" ")[1]
    & $cmd $arg "$ScriptDir\main.py" @args
} else {
    & $PythonExe "$ScriptDir\main.py" @args
}
exit $LASTEXITCODE
