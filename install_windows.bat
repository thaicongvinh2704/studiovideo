@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3 -m venv .venv
  if errorlevel 1 (
    echo Can Python 3.11 hoac 3.12 x64 tu python.org. Cai va chay lai.
    pause
    exit /b 1
  )
)
".venv\Scripts\python.exe" -X utf8 -m pip install -r requirements.txt
if errorlevel 1 goto failed
".venv\Scripts\python.exe" -X utf8 tools\download_voice.py
if errorlevel 1 goto failed
if not exist "examples\yellow_umbrella\project.json" ".venv\Scripts\python.exe" -X utf8 tools\create_demo.py
echo Cai xong. FFmpeg can nam tren PATH hoac bin\ffmpeg.exe va bin\ffprobe.exe.
echo Mo start_studio.bat de su dung offline.
pause
exit /b 0
:failed
echo Cai dat that bai. Kiem tra internet va thong bao loi phia tren.
pause
exit /b 1
