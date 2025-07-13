# 🚀 Running the Walmart AI Forecasting System

## Quick Start

### Option 1: Automatic Startup (Recommended)
1. **Double-click** `start-app.bat` or right-click `start-app.ps1` and select "Run with PowerShell"
2. Wait for both servers to start
3. Open your browser to `http://localhost:3000` (or the port shown)

### Option 2: Manual Startup

#### Start Backend (Flask API)
```powershell
cd backend
python app.py
```

#### Start Frontend (React App) - In a new terminal
```powershell
cd walmart-forecast-frontend
npm start
```

## 🌐 Access Points
- **Frontend Dashboard**: http://localhost:3000 (or 3001 if 3000 is busy)
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 🔧 Troubleshooting

### Common Issues

#### 1. "Cannot read properties of undefined (reading 'length')"
✅ **FIXED** - This was caused by components trying to access undefined data. All components now have proper null checks.

#### 2. Port 3000 already in use
- The app will automatically use port 3001 or 3002
- Check the terminal output for the correct port

#### 3. Backend not starting
- Make sure you're in the `backend` directory
- Check if Python is installed: `python --version`
- Install requirements: `pip install -r requirements.txt`

#### 4. Frontend not starting
- Make sure you're in the `walmart-forecast-frontend` directory
- Install dependencies: `npm install`
- Check if Node.js is installed: `node --version`

#### 5. PowerShell syntax errors
- Use separate commands instead of `&&`
- Or use the provided `.bat` or `.ps1` files

### Testing the Application

1. **Generate a Forecast**:
   - Select SKUs and Stores
   - Choose forecast period (7-60 days)
   - Select model type (ARIMA/LSTM)
   - Click "Generate Forecast"

2. **View Analytics**:
   - Switch between tabs to see different views
   - Check the Forecast Analytics tab for charts
   - View Inventory Management for suggestions

3. **Test Features**:
   - Weather Widget (select stores first)
   - Store Performance
   - Simulation Tools (requires forecast data)

## 🎨 UI Features

### Enhanced Design
- **Modern Dark Theme** with Walmart brand colors
- **Google Fonts** (Inter) for professional typography
- **Smooth Animations** and hover effects
- **Responsive Design** for all screen sizes
- **Interactive Charts** with Recharts
- **Gradient Backgrounds** and modern styling

### Components
- **Dashboard Overview**: Main dashboard with quick stats
- **Forecast Analytics**: Interactive charts and trends
- **Inventory Management**: Smart suggestions and alerts
- **Store Performance**: Performance metrics
- **Simulation Tools**: What-if scenario analysis
- **Weather Widget**: Weather data integration

## 📊 API Endpoints

The backend provides these endpoints:
- `POST /api/forecast` - Generate demand forecasts
- `POST /api/inventory-suggestions` - Get inventory recommendations
- `GET /api/store-performance` - Store performance metrics
- `GET /api/weather-data` - Weather information
- `POST /api/simulation` - Run what-if simulations
- `GET /api/health` - Health check

## 🛠️ Development

### Backend (Flask)
- **Location**: `backend/`
- **Main file**: `app.py`
- **Models**: `models/forecasting_models.py`
- **Utilities**: `utils/`

### Frontend (React)
- **Location**: `walmart-forecast-frontend/`
- **Main component**: `src/components/Dashboard.js`
- **Charts**: `src/components/ForecastChart.js`
- **API**: `src/services/api.js`

## 🎉 Enjoy Your AI Forecasting System!

The application is now ready with:
- ✅ Fixed null/undefined errors
- ✅ Enhanced UI with modern design
- ✅ Proper error handling
- ✅ Responsive layout
- ✅ Professional typography
- ✅ Smooth animations

Generate your first forecast and explore the powerful analytics dashboard! 