# Quick start script for the UniHub API on Windows PowerShell.
# Works from any directory:  .\backend\start_api.ps1
# If scripts are blocked:    powershell -ExecutionPolicy Bypass -File backend\start_api.ps1
$ErrorActionPreference = "Stop"

# Always run from this script's directory (backend\), wherever it was called from.
Set-Location $PSScriptRoot

$venvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment in backend\venv..."
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3 -m venv venv
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        python -m venv venv
    } else {
        Write-Error "Python 3 is not installed. Install Python 3.10+ from https://www.python.org/downloads/ and tick 'Add python.exe to PATH'."
    }
    if ($LASTEXITCODE -ne 0) { Write-Error "Creating the virtual environment failed." }
}

Write-Host "Installing dependencies..."
& $venvPython -m pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) { Write-Error "Installing dependencies failed." }

Write-Host ""
Write-Host "Starting API server..."
Write-Host "   API:  http://localhost:8084"
Write-Host "   Docs: http://localhost:8084/docs"
Write-Host "Press Ctrl+C to stop the server"
Write-Host ""

# Calling the venv's python directly avoids Activate.ps1, which the execution policy may block.
& $venvPython -m uvicorn app.main:app --host 0.0.0.0 --port 8084
