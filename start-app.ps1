# Walmart AI Forecasting System - Startup Script
# This script starts both the backend Flask API and frontend React app

Write-Host "🚀 Starting Walmart AI Forecasting System..." -ForegroundColor Green
Write-Host ""

# Function to check if a port is in use
function Test-Port {
    param($Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

# Function to find an available port
function Find-AvailablePort {
    param($StartPort)
    $port = $StartPort
    while (Test-Port -Port $port) {
        $port++
    }
    return $port
}

# Check if backend port 5000 is available
if (Test-Port -Port 5000) {
    Write-Host "⚠️  Port 5000 is already in use. Backend might already be running." -ForegroundColor Yellow
} else {
    Write-Host "✅ Port 5000 is available for backend" -ForegroundColor Green
}

# Check if frontend port 3000 is available
$frontendPort = 3000
if (Test-Port -Port $frontendPort) {
    $frontendPort = Find-AvailablePort -StartPort 3001
    Write-Host "⚠️  Port 3000 is in use. Frontend will use port $frontendPort" -ForegroundColor Yellow
} else {
    Write-Host "✅ Port 3000 is available for frontend" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Starting servers..." -ForegroundColor Cyan
Write-Host ""

# Start Backend (Flask API)
Write-Host "🔧 Starting Backend (Flask API) on port 5000..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python app.py" -WindowStyle Normal

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start Frontend (React App)
Write-Host "🎨 Starting Frontend (React App) on port $frontendPort..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd walmart-forecast-frontend; npm start" -WindowStyle Normal

Write-Host ""
Write-Host "✅ Both servers are starting..." -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access your application at:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:$frontendPort" -ForegroundColor White
Write-Host "   Backend API: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "📊 Dashboard Features:" -ForegroundColor Cyan
Write-Host "   • AI-powered demand forecasting" -ForegroundColor White
Write-Host "   • Interactive charts and analytics" -ForegroundColor White
Write-Host "   • Inventory management suggestions" -ForegroundColor White
Write-Host "   • Store performance metrics" -ForegroundColor White
Write-Host "   • Weather integration" -ForegroundColor White
Write-Host "   • Simulation tools" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop the servers, close the PowerShell windows or press Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 Enjoy your Walmart AI Forecasting System!" -ForegroundColor Green 