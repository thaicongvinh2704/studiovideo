@echo off
cd /d "%~dp0"
python -X utf8 scripts\setup.py
if errorlevel 1 goto failed
echo Da cai dat. Chay START_STUDIO.cmd.
pause
exit /b 0
:failed
echo Cai dat chua thanh cong. Kiem tra thong bao o tren.
pause
exit /b 1
