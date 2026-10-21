@echo off
setlocal
set "studioFilmExe=%~dp0..\..\dist\StickmanAnimationStudio\StickmanAnimationStudio.exe"
if exist "%studioFilmExe%" (
    start "" "%studioFilmExe%" "%~dp0project.json"
) else (
    "%~dp0..\..\..\.venv\Scripts\python.exe" "%~dp0..\..\main.py" "%~dp0project.json"
)
endlocal
