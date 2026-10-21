@echo off
setlocal
set "historyClipStudio=%~dp0..\..\dist\StickmanAnimationStudio\StickmanAnimationStudio.exe"
start "" "%historyClipStudio%" "%~dp0project.json"
endlocal
