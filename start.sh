#!/bin/bash

echo "Starting Walmart AI-Driven Demand Forecasting System..."
echo

echo "Starting Backend Server..."
cd backend
python app.py &
BACKEND_PID=$!

echo
echo "Starting Frontend Server..."
cd ../walmart-forecast-frontend
npm start &
FRONTEND_PID=$!

echo
echo "System starting up..."
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop both servers..."

# Wait for user to stop
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 