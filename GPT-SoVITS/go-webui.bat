@echo off
set "SCRIPT_DIR=%~dp0"
set ENV_NAME=GPTSoVits
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
cd /d "%SCRIPT_DIR%"
CALL D:\Anaconda\Scripts\activate.bat
CALL conda activate %ENV_NAME%
python webui.py zh_CN
pause
