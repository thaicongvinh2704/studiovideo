param([string]$StudioPython = 'projects/angkor_wat_1min/.venv/Scripts/python.exe')
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $repoRoot
$toolRoot = Join-Path $repoRoot '.deps/editing'
New-Item -ItemType Directory -Force "$toolRoot/downloads", "$toolRoot/ollama", '.cache/pip' | Out-Null
$env:PIP_CACHE_DIR = Join-Path $repoRoot '.cache/pip'
function Check-Exit { if ($LASTEXITCODE -ne 0) { throw "Command failed: $LASTEXITCODE" } }
& $StudioPython -m venv "$toolRoot/whisperx"
Check-Exit
$alignPython = "$toolRoot/whisperx/Scripts/python.exe"
& $alignPython -m pip install --upgrade pip
Check-Exit
& $alignPython -m pip install torch==2.8.0 torchaudio==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cpu
Check-Exit
& $alignPython -m pip install -r requirements-editing-whisperx.txt
Check-Exit

if (-not (Test-Path "$toolRoot/ollama/ollama.exe")) {
    $archive = "$toolRoot/downloads/ollama-windows-amd64-0.40.10.zip"
    curl.exe --fail --location --retry 3 --output $archive https://github.com/ollama/ollama/releases/download/v0.40.10/ollama-windows-amd64.zip
    Check-Exit
    Expand-Archive -LiteralPath $archive -DestinationPath "$toolRoot/ollama" -Force
}
if (-not (Test-Path "$env:ProgramFiles/Glaxnimate/bin/glaxnimate.exe")) {
    $installer = "$toolRoot/downloads/glaxnimate-0.6.0-x86_64.exe"
    curl.exe --fail --location --retry 3 --output $installer https://download.kde.org/stable/glaxnimate/0.6.0/windows/glaxnimate-0.6.0-x86_64.exe
    Check-Exit
    $signature = Get-AuthenticodeSignature -LiteralPath $installer
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'K Desktop Environment') {
        throw 'KDE installer signature was not verified.'
    }
    $installation = Start-Process -FilePath $installer -ArgumentList '/S' -WindowStyle Hidden -Wait -PassThru
    if ($installation.ExitCode -ne 0) { throw 'Glaxnimate installer failed.' }
}
# Repair the missing embedded Python stdlib in the official KDE Windows package.
if (-not (Test-Path "$toolRoot/python311/Lib/encodings")) {
    New-Item -ItemType Directory -Force "$toolRoot/python311/Lib" | Out-Null
    $pythonArchive = "$toolRoot/downloads/python-3.11.9-embed-amd64.zip"
    curl.exe --fail --location --retry 3 --output $pythonArchive https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip
    Check-Exit
    Expand-Archive -LiteralPath $pythonArchive -DestinationPath "$toolRoot/python311" -Force
    Expand-Archive -LiteralPath "$toolRoot/python311/python311.zip" -DestinationPath "$toolRoot/python311/Lib" -Force
}
& $StudioPython -X utf8 tools/editing_tools.py start-vision
Check-Exit
$env:OLLAMA_HOST = '127.0.0.1:11435'
$env:OLLAMA_MODELS = Join-Path $repoRoot '.models/editing/ollama'
$env:OLLAMA_NO_CLOUD = '1'
& "$toolRoot/ollama/ollama.exe" pull qwen3-vl:2b-instruct
Check-Exit
& $StudioPython -X utf8 tools/editing_tools.py doctor
Check-Exit
Write-Output 'Models for Vietnamese forced alignment download on first alignment. See docs/EDITING_TOOLS.md.'
