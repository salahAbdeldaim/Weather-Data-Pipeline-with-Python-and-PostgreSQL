@echo off
echo ========================================================
echo   Stopping Weather Data Pipeline Docker Services...
echo ========================================================
cd /d "%~dp0"
docker compose down
echo.
echo All services stopped cleanly.
pause
