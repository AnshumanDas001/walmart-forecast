@echo off
echo Starting Walmart AI-Driven Demand Forecasting System...
echo.

echo Starting Backend Server...
cd backend
start "Backend Server" python app.py

echo.
echo Starting Frontend Server...
cd ..\walmart-forecast-frontend
start "Frontend Server" npm start

echo.
echo System starting up...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause 