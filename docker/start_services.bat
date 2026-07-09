@echo off
echo ========================================================
echo   Starting Weather Data Pipeline Docker Services...
echo ========================================================
cd /d "%~dp0"
docker compose up -d
echo.
echo Services status:
docker compose ps
echo.
echo Metabase BI is accessible at: http://localhost:3000
echo PostgreSQL Database is accessible at: localhost:5432
pause
