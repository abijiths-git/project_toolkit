@echo off
REM Get the directory where the batch file is located
set BAT_DIR=%~dp0

REM Clean the downloads folder
echo Cleaning Downloads folder...
rmdir /s /q "%BAT_DIR%downloads" > nul
mkdir "%BAT_DIR%downloads"
echo Downloads folder cleaned.

@echo off
cd /d T:\001_Treffer\speedgrip_chuck_co\000_designers\sujith\02_phase_2\Mounting plates (low profile)\py dwlds
python sg_download.py
pause