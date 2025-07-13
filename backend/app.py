from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import requests
from models.forecasting_models import ARIMAModel, LSTMModel
from utils.data_processor import DataProcessor
from utils.external_apis import WeatherAPI, HolidayAPI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=['*'], methods=['GET', 'POST', 'PUT', 'DELETE'], allow_headers=['Content-Type'])

# Initialize models and APIs
data_processor = DataProcessor()
weather_api = WeatherAPI()
holiday_api = HolidayAPI()

# Global model instances
arima_model = ARIMAModel()
lstm_model = LSTMModel()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Walmart Forecasting API is running"})

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint"""
    return jsonify({
        'message': 'Backend is working!',
        'timestamp': datetime.now().isoformat(),
        'status': 'success'
    })

@app.route('/api/debug', methods=['GET'])
def debug_info():
    """Debug endpoint to check system status"""
    try:
        # Test data processor
        test_data = data_processor.get_historical_data(['SKU001'], ['STORE001'])
        
        # Test weather API
        test_weather = weather_api.get_weather_forecast(['STORE001'], 7)
        
        # Test holiday API
        test_holidays = holiday_api.get_holidays(7)
        
        return jsonify({
            'status': 'healthy',
            'data_processor': 'working',
            'weather_api': 'working',
            'holiday_api': 'working',
            'test_data_keys': list(test_data.keys()),
            'test_weather_keys': list(test_weather.keys()),
            'test_holidays_count': len(test_holidays)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'traceback': str(e.__class__.__name__)
        }), 500

@app.route('/api/forecast', methods=['POST'])
def generate_forecast():
    """Generate demand forecast for given SKUs and stores"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
            
        sku_ids = data.get('sku_ids', [])
        store_ids = data.get('store_ids', [])
        forecast_days = data.get('forecast_days', 30)
        model_type = data.get('model_type', 'arima')  # Changed default to arima
        
        if not sku_ids or not store_ids:
            return jsonify({'success': False, 'error': 'SKU IDs and Store IDs are required'}), 400
        
        print(f"Generating forecast for SKUs: {sku_ids}, Stores: {store_ids}, Days: {forecast_days}, Model: {model_type}")
        
        # Get historical data
        historical_data = data_processor.get_historical_data(sku_ids, store_ids)
        print(f"Historical data keys: {list(historical_data.keys())}")
        
        # Get external factors
        weather_data = weather_api.get_weather_forecast(store_ids, forecast_days)
        holiday_data = holiday_api.get_holidays(forecast_days)
        
        # Generate forecasts
        forecasts = {}
        for sku_id in sku_ids:
            for store_id in store_ids:
                key = f"{sku_id}_{store_id}"
                print(f"Processing forecast for key: {key}")
                
                if key not in historical_data:
                    print(f"Warning: No historical data for key {key}")
                    continue
                
                try:
                    if model_type == 'lstm':
                        forecast = lstm_model.predict(
                            historical_data[key], 
                            weather_data.get(store_id, []), 
                            holiday_data, 
                            forecast_days
                        )
                    else:
                        forecast = arima_model.predict(
                            historical_data[key], 
                            weather_data.get(store_id, []), 
                            holiday_data, 
                            forecast_days
                        )
                    
                    forecasts[key] = {
                        'sku_id': sku_id,
                        'store_id': store_id,
                        'forecast': forecast['forecast'],
                        'confidence_interval': forecast.get('confidence_interval', {}),
                        'feature_importance': forecast.get('feature_importance', {})
                    }
                    print(f"Successfully generated forecast for {key}")
                    
                except Exception as model_error:
                    print(f"Error generating forecast for {key}: {str(model_error)}")
                    # Use simple fallback forecast
                    forecasts[key] = {
                        'sku_id': sku_id,
                        'store_id': store_id,
                        'forecast': [50] * forecast_days,  # Simple fallback
                        'confidence_interval': {
                            'lower': [40] * forecast_days,
                            'upper': [60] * forecast_days
                        },
                        'feature_importance': {
                            'model_type': 'Fallback',
                            'error': str(model_error)
                        }
                    }
        
        if not forecasts:
            return jsonify({'success': False, 'error': 'No forecasts generated'}), 500
        
        return jsonify({
            'success': True,
            'forecasts': forecasts,
            'model_used': model_type,
            'forecast_days': forecast_days
        })
        
    except Exception as e:
        print(f"Forecast generation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/simulation', methods=['POST'])
def run_simulation():
    """Run what-if simulations"""
    try:
        data = request.get_json()
        base_forecast = data.get('base_forecast', {})
        scenario = data.get('scenario', {})
        
        # Apply scenario changes
        modified_forecast = data_processor.apply_scenario(base_forecast, scenario)
        
        return jsonify({
            'success': True,
            'original_forecast': base_forecast,
            'modified_forecast': modified_forecast,
            'scenario_applied': scenario
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/inventory-suggestions', methods=['POST'])
def get_inventory_suggestions():
    """Generate inventory suggestions based on forecasts"""
    try:
        data = request.get_json()
        forecasts = data.get('forecasts', {})
        current_inventory = data.get('current_inventory', {})
        
        suggestions = data_processor.generate_inventory_suggestions(
            forecasts, current_inventory
        )
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/store-performance', methods=['GET'])
def get_store_performance():
    """Get historical performance metrics for stores"""
    try:
        store_ids = request.args.get('store_ids', '').split(',')
        days = int(request.args.get('days', 30))
        
        performance_data = data_processor.get_store_performance(store_ids, days)
        
        return jsonify({
            'success': True,
            'performance': performance_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sku-analytics', methods=['GET'])
def get_sku_analytics():
    """Get SKU-level analytics and trends"""
    try:
        sku_id = request.args.get('sku_id')
        store_id = request.args.get('store_id')
        days = int(request.args.get('days', 90))
        
        analytics = data_processor.get_sku_analytics(sku_id, store_id, days)
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/weather-data', methods=['GET'])
def get_weather_data():
    """Get current weather data for stores"""
    try:
        store_ids = request.args.get('store_ids', '').split(',')
        weather_data = weather_api.get_current_weather(store_ids)
        
        return jsonify({
            'success': True,
            'weather': weather_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 