@echo off
echo ========================================================
echo   Running Weather ETL Pipeline (Extract & Load)...
echo ========================================================
cd /d "%~dp0"
docker compose start weather-etl
echo.
echo Following pipeline logs:
docker compose logs -f weather-etl
pause
