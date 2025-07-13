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
CORS(app)

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

@app.route('/api/forecast', methods=['POST'])
def generate_forecast():
    """Generate demand forecast for given SKUs and stores"""
    try:
        data = request.get_json()
        sku_ids = data.get('sku_ids', [])
        store_ids = data.get('store_ids', [])
        forecast_days = data.get('forecast_days', 30)
        model_type = data.get('model_type', 'lstm')  # 'lstm' or 'arima'
        
        # Get historical data
        historical_data = data_processor.get_historical_data(sku_ids, store_ids)
        
        # Get external factors
        weather_data = weather_api.get_weather_forecast(store_ids, forecast_days)
        holiday_data = holiday_api.get_holidays(forecast_days)
        
        # Generate forecasts
        forecasts = {}
        for sku_id in sku_ids:
            for store_id in store_ids:
                key = f"{sku_id}_{store_id}"
                
                if model_type == 'lstm':
                    forecast = lstm_model.predict(
                        historical_data[key], 
                        weather_data[store_id], 
                        holiday_data, 
                        forecast_days
                    )
                else:
                    forecast = arima_model.predict(
                        historical_data[key], 
                        weather_data[store_id], 
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
        
        return jsonify({
            'success': True,
            'forecasts': forecasts,
            'model_used': model_type,
            'forecast_days': forecast_days
        })
        
    except Exception as e:
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