@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\pythonw.exe" (
  start "" ".venv\Scripts\pythonw.exe" "main.py" %*
  exit /b
)
if exist "..\.venv\Scripts\pythonw.exe" (
  start "" "..\.venv\Scripts\pythonw.exe" "main.py" %*
  exit /b
)
if exist "projects\angkor_wat_1min\.venv\Scripts\pythonw.exe" (
  start "" "projects\angkor_wat_1min\.venv\Scripts\pythonw.exe" "main.py" %*
  exit /b
)
if exist "dist\StickmanAnimationStudio\StickmanAnimationStudio.exe" (
  start "" "dist\StickmanAnimationStudio\StickmanAnimationStudio.exe" %*
  exit /b
)
echo Chua cai dependency. Hay chay install_windows.bat.
pause
