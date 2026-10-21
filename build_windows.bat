@echo off
setlocal
cd /d "%~dp0"
set "STUDIO_PY=.venv\Scripts\python.exe"
if not exist "%STUDIO_PY%" set "STUDIO_PY=..\.venv\Scripts\python.exe"
if not exist "%STUDIO_PY%" (
  echo Chay install_windows.bat truoc.
  pause
  exit /b 1
)
"%STUDIO_PY%" -X utf8 tools\prepare_build.py
if errorlevel 1 goto failed
"%STUDIO_PY%" -X utf8 -m PyInstaller --noconfirm StickmanAnimationStudio.spec
if errorlevel 1 goto failed
"%STUDIO_PY%" -X utf8 tools\package_runtime.py
if errorlevel 1 goto failed
echo Build xong: dist\StickmanAnimationStudio\StickmanAnimationStudio.exe
pause
exit /b 0
:failed
echo Build that bai. Xem log phia tren.
pause
exit /b 1
