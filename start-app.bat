@echo off
title Walmart AI Forecasting System - Startup

echo.
echo ========================================
echo   Walmart AI Forecasting System
echo ========================================
echo.

echo Starting Backend (Flask API)...
start "Backend Server" cmd /k "cd backend && python app.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Frontend (React App)...
start "Frontend Server" cmd /k "cd walmart-forecast-frontend && npm start"

echo.
echo ========================================
echo   Servers are starting...
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:5000
echo.
echo Close the command windows to stop the servers
echo.
pause 