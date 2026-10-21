@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\pythonw.exe" (
  start "" ".venv\Scripts\pythonw.exe" "tools\open_drawing_desk.py" %*
  exit /b
)
if exist "..\.venv\Scripts\pythonw.exe" (
  start "" "..\.venv\Scripts\pythonw.exe" "tools\open_drawing_desk.py" %*
  exit /b
)
if exist "projects\angkor_wat_1min\.venv\Scripts\pythonw.exe" (
  start "" "projects\angkor_wat_1min\.venv\Scripts\pythonw.exe" "tools\open_drawing_desk.py" %*
  exit /b
)
echo Chua tim thay Python co PySide6. Hay chay install_windows.bat.
pause
