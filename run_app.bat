@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo       LANEGUARD VISION - STARTUP
echo ==========================================

echo [1/4] Closing any old app instances...
taskkill /F /IM python.exe /T >nul 2>&1

echo [2/4] Verifying dependencies...
python -m pip install -r backend/requirements.txt --quiet

echo [3/4] Starting Backend Server...
echo (This window must stay open)
start /min cmd /c "python -m backend.main"

echo [4/4] Launching Dashboard...
echo Waiting for backend to initialize...
timeout /t 8 >nul
start http://localhost:8000

echo Done! App is running.
echo If the camera doesn't show up, wait 5 seconds and refresh the browser.
pause
