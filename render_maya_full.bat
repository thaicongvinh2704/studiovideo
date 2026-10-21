@echo off
cd /d "%~dp0"
echo Dang render toan bo video van minh Maya (13 phut 51 giay, 1080p)...
call .venv\Scripts\python.exe -X utf8 tools\render_full_maya_video.py
pause
