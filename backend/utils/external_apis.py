import requests
import json
from datetime import datetime, timedelta
import random

class WeatherAPI:
    def __init__(self):
        self.api_key = "demo_key"  # Replace with actual API key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, store_ids):
        """Get current weather for stores"""
        weather_data = {}
        
        for store_id in store_ids:
            # Simulate weather data for demo
            conditions = ['clear', 'rain', 'cloudy']
            weather_data[store_id] = {
                'temperature': random.randint(15, 35),
                'humidity': random.randint(30, 80),
                'wind_speed': random.randint(5, 25),
                'visibility': random.randint(5, 15),
                'weather_condition': random.choice(conditions),
                'pressure': random.randint(1000, 1020)
            }
        
        return weather_data
    
    def get_weather_forecast(self, store_ids, days):
        """Get weather forecast for stores"""
        forecast_data = {}
        
        for store_id in store_ids:
            forecast_data[store_id] = []
            for i in range(days):
                conditions = ['clear', 'rain', 'cloudy']
                forecast_data[store_id].append({
                    'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                    'temperature': random.randint(15, 35),
                    'humidity': random.randint(30, 80),
                    'wind_speed': random.randint(5, 25),
                    'weather_condition': random.choice(conditions)
                })
        
        return forecast_data

class HolidayAPI:
    def __init__(self):
        self.holidays = {
            '2024-12-25': {
                'name': 'Christmas',
                'type': 'major',
                'impact': {
                    'SKU001': 2.8,  # Coffee beans - high demand
                    'SKU002': 1.5,  # Milk - moderate
                    'SKU003': 2.2,  # Bread - high
                    'SKU004': 1.8,  # Bananas - moderate
                    'SKU005': 3.0   # Chicken - very high
                }
            },
            '2024-12-31': {
                'name': 'New Year\'s Eve',
                'type': 'major',
                'impact': {
                    'SKU001': 2.0,  # Coffee - high
                    'SKU002': 1.3,  # Milk - low
                    'SKU003': 1.6,  # Bread - moderate
                    'SKU004': 1.2,  # Bananas - low
                    'SKU005': 2.5   # Chicken - high
                }
            },
            '2025-02-14': {
                'name': 'Valentine\'s Day',
                'type': 'minor',
                'impact': {
                    'SKU001': 1.8,  # Coffee - moderate
                    'SKU002': 1.4,  # Milk - moderate
                    'SKU003': 1.3,  # Bread - low
                    'SKU004': 1.1,  # Bananas - low
                    'SKU005': 1.9   # Chicken - moderate
                }
            },
            '2024-11-28': {
                'name': 'Thanksgiving',
                'type': 'major',
                'impact': {
                    'SKU001': 2.2,  # Coffee - high
                    'SKU002': 1.6,  # Milk - moderate
                    'SKU003': 2.5,  # Bread - very high
                    'SKU004': 1.9,  # Bananas - moderate
                    'SKU005': 3.2   # Chicken - very high
                }
            },
            '2024-11-29': {
                'name': 'Black Friday',
                'type': 'major',
                'impact': {
                    'SKU001': 2.5,  # Coffee - high
                    'SKU002': 1.8,  # Milk - moderate
                    'SKU003': 2.0,  # Bread - high
                    'SKU004': 1.5,  # Bananas - moderate
                    'SKU005': 2.8   # Chicken - high
                }
            },
            '2024-07-04': {
                'name': 'Independence Day',
                'type': 'minor',
                'impact': {
                    'SKU001': 1.6,  # Coffee - moderate
                    'SKU002': 1.4,  # Milk - moderate
                    'SKU003': 1.5,  # Bread - moderate
                    'SKU004': 1.3,  # Bananas - moderate
                    'SKU005': 2.0   # Chicken - high
                }
            }
        }
    
    def get_holidays(self, days):
        """Get holidays for the next N days"""
        holidays = []
        start_date = datetime.now()
        
        for i in range(days):
            date_str = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            if date_str in self.holidays:
                holiday = self.holidays[date_str].copy()
                holiday['date'] = date_str
                holidays.append(holiday)
        
        return holidays
    
    def get_holiday_impact(self, sku_id, date):
        """Get holiday impact for specific SKU and date"""
        date_str = date.strftime('%Y-%m-%d') if isinstance(date, datetime) else date
        
        if date_str in self.holidays:
            return self.holidays[date_str]['impact'].get(sku_id, 1.0)
        
        return 1.0  # No holiday impact
    
    def get_upcoming_holidays(self, days=30):
        """Get upcoming holidays with their impact data"""
        upcoming = []
        start_date = datetime.now()
        
        for i in range(days):
            date_str = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            if date_str in self.holidays:
                holiday = self.holidays[date_str].copy()
                holiday['date'] = date_str
                holiday['days_until'] = i
                upcoming.append(holiday)
        
        return upcoming 