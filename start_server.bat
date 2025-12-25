@echo off
TITLE GestureNav Vision Server
CLS

:: Ensure we are in the script's directory
cd /d "%~dp0"

:: ---------------------------------------------------------
:: STEP 1: Check if Python is installed
:: ---------------------------------------------------------
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO NoPython

:: ---------------------------------------------------------
:: STEP 2: Check for Libraries
:: ---------------------------------------------------------
echo [1/3] Checking System Integrity...
python -c "import mediapipe; import cv2; import numpy" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO InstallDeps

echo [OK] Libraries found.
GOTO CheckModel

:InstallDeps
echo.
echo [!] First-time setup detected (Missing Libraries).
echo [!] Installing AI Dependencies... Please wait.
echo.
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 GOTO InstallFailed
echo.
echo [SUCCESS] Dependencies installed.

:CheckModel
:: ---------------------------------------------------------
:: STEP 3: Sanity Check for Model 
:: ---------------------------------------------------------
IF EXIST "server\hand_landmarker.task" GOTO Launch
echo [!] Model file missing. Downloading...
python server/download_model.py
IF %ERRORLEVEL% NEQ 0 GOTO DownloadFailed
echo [OK] AI Model found.

:Launch
:: ---------------------------------------------------------
:: STEP 4: Launch
:: ---------------------------------------------------------
echo.
echo [3/3] Starting Vision Engine...
echo =======================================================
echo    GestureNav Server is Running.
echo    Keep this window open!
echo =======================================================
echo.
python server/main.py
pause
exit

:: ---------------------------------------------------------
:: ERROR HANDLERS
:: ---------------------------------------------------------

:NoPython
echo [ERROR] Python is not installed or not in your PATH.
echo Please install Python 3.10+ from python.org
echo.
pause
exit

:InstallFailed
echo [ERROR] Failed to install dependencies.
echo Please ensure you have internet access and pip is installed.
pause
exit

:DownloadFailed
echo [ERROR] Failed to download model.
pause
exit
