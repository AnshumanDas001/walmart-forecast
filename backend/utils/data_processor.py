import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataProcessor:
    def __init__(self):
        self.sku_info = {
            'SKU001': {'name': 'Coffee Beans', 'category': 'Beverages', 'base_price': 12.99},
            'SKU002': {'name': 'Milk', 'category': 'Dairy', 'base_price': 3.49},
            'SKU003': {'name': 'Bread', 'category': 'Bakery', 'base_price': 2.99},
            'SKU004': {'name': 'Bananas', 'category': 'Produce', 'base_price': 1.99},
            'SKU005': {'name': 'Chicken Breast', 'category': 'Meat', 'base_price': 8.99}
        }
        
        self.store_info = {
            'STORE001': {'name': 'Downtown Store', 'location': 'New York', 'size': 'large'},
            'STORE002': {'name': 'Suburban Store', 'location': 'Los Angeles', 'size': 'medium'},
            'STORE003': {'name': 'Mall Store', 'location': 'Chicago', 'size': 'small'}
        }
    
    def get_historical_data(self, sku_ids, store_ids):
        """Get historical sales data for SKUs and stores"""
        data = {}
        
        for sku_id in sku_ids:
            for store_id in store_ids:
                key = f"{sku_id}_{store_id}"
                
                # Generate realistic historical data
                base_demand = self._get_base_demand(sku_id, store_id)
                dates = self._generate_dates(90)  # 90 days of historical data
                sales = self._generate_sales_data(base_demand, dates, sku_id, store_id)
                
                data[key] = {
                    'sku_id': sku_id,
                    'store_id': store_id,
                    'date': dates,
                    'sales': sales,
                    'sku_info': self.sku_info.get(sku_id, {}),
                    'store_info': self.store_info.get(store_id, {})
                }
        
        return data
    
    def _get_base_demand(self, sku_id, store_id):
        """Get base demand for SKU-store combination"""
        base_demands = {
            'SKU001': {'STORE001': 45, 'STORE002': 38, 'STORE003': 32},
            'SKU002': {'STORE001': 120, 'STORE002': 95, 'STORE003': 78},
            'SKU003': {'STORE001': 85, 'STORE002': 72, 'STORE003': 58},
            'SKU004': {'STORE001': 65, 'STORE002': 55, 'STORE003': 42},
            'SKU005': {'STORE001': 35, 'STORE002': 28, 'STORE003': 22}
        }
        
        return base_demands.get(sku_id, {}).get(store_id, 50)
    
    def _generate_dates(self, days):
        """Generate list of dates"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
        
        return dates
    
    def _generate_sales_data(self, base_demand, dates, sku_id, store_id):
        """Generate realistic sales data with trends and seasonality"""
        sales = []
        
        for i, date in enumerate(dates):
            # Base demand
            demand = base_demand
            
            # Add weekly seasonality (weekend effect)
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            if date_obj.weekday() >= 5:  # Weekend
                demand *= 1.3
            
            # Add monthly trend (slight growth)
            trend_factor = 1 + (i * 0.001)
            demand *= trend_factor
            
            # Add random variation
            variation = random.normalvariate(1, 0.15)
            demand *= variation
            
            # Ensure non-negative values
            demand = max(0, demand)
            
            sales.append(round(demand))
        
        return sales
    
    def apply_scenario(self, base_forecast, scenario):
        """Apply scenario changes to forecast"""
        modified_forecast = base_forecast.copy()
        
        if not modified_forecast or 'forecasts' not in modified_forecast:
            return modified_forecast
        
        for key, forecast in modified_forecast['forecasts'].items():
            if 'forecast' not in forecast:
                continue
                
            # Apply scenario multipliers
            weather_multiplier = scenario.get('weather_impact', 1.0)
            promotion_multiplier = scenario.get('promotion_impact', 1.0)
            holiday_multiplier = scenario.get('holiday_impact', 1.0)
            price_change = scenario.get('price_change', 0)
            competitor_action = scenario.get('competitor_action', 'none')
            
            # Calculate price impact (inverse relationship)
            price_multiplier = 1 / (1 + (price_change / 100))
            
            # Calculate competitor impact
            competitor_impacts = {
                'none': 1.0,
                'price_cut': 0.8,
                'promotion': 0.9,
                'new_product': 0.7,
                'aggressive': 0.6
            }
            competitor_multiplier = competitor_impacts.get(competitor_action, 1.0)
            
            # Apply total impact
            total_multiplier = (weather_multiplier * promotion_multiplier * 
                              holiday_multiplier * price_multiplier * competitor_multiplier)
            
            # Apply to forecast values
            forecast['forecast'] = [max(0, val * total_multiplier) for val in forecast['forecast']]
            
            # Update confidence intervals if they exist
            if 'confidence_interval' in forecast:
                if 'lower' in forecast['confidence_interval']:
                    forecast['confidence_interval']['lower'] = [
                        max(0, val * total_multiplier) for val in forecast['confidence_interval']['lower']
                    ]
                if 'upper' in forecast['confidence_interval']:
                    forecast['confidence_interval']['upper'] = [
                        max(0, val * total_multiplier) for val in forecast['confidence_interval']['upper']
                    ]
        
        return modified_forecast
    
    def generate_inventory_suggestions(self, forecasts, current_inventory):
        """Generate inventory suggestions based on forecasts"""
        suggestions = {}
        
        if not forecasts or 'forecasts' not in forecasts:
            return suggestions
        
        for key, forecast in forecasts['forecasts'].items():
            if 'forecast' not in forecast:
                continue
                
            # Calculate total forecasted demand
            total_demand = sum(forecast['forecast'])
            
            # Get current inventory
            current_stock = current_inventory.get(key, 0)
            
            # Calculate suggested inventory
            safety_stock = total_demand * 0.2  # 20% safety stock
            suggested_inventory = total_demand + safety_stock
            
            # Determine action needed
            if current_stock < suggested_inventory * 0.8:
                action = 'restock'
                urgency = 'high' if current_stock < suggested_inventory * 0.5 else 'medium'
            elif current_stock > suggested_inventory * 1.2:
                action = 'reduce'
                urgency = 'high' if current_stock > suggested_inventory * 1.5 else 'medium'
            else:
                action = 'maintain'
                urgency = 'low'
            
            suggestions[key] = {
                'sku_id': forecast.get('sku_id', ''),
                'store_id': forecast.get('store_id', ''),
                'current_inventory': current_stock,
                'forecasted_demand': round(total_demand),
                'suggested_inventory': round(suggested_inventory),
                'action': action,
                'urgency': urgency,
                'order_quantity': max(0, round(suggested_inventory - current_stock)) if action == 'restock' else 0
            }
        
        return suggestions
    
    def get_store_performance(self, store_ids, days=30):
        """Get historical performance metrics for stores"""
        performance = {}
        
        for store_id in store_ids:
            # Generate performance metrics
            total_sales = random.randint(50000, 200000)
            avg_transaction = random.uniform(45, 85)
            customer_count = random.randint(800, 2000)
            
            # Calculate efficiency score
            efficiency_score = random.uniform(0.7, 0.95)
            
            performance[store_id] = {
                'total_sales': total_sales,
                'avg_transaction': round(avg_transaction, 2),
                'customer_count': customer_count,
                'efficiency_score': round(efficiency_score, 3),
                'performance_trend': 'improving' if efficiency_score > 0.85 else 'stable',
                'store_info': self.store_info.get(store_id, {})
            }
        
        return performance
    
    def get_sku_analytics(self, sku_id, store_id, days=90):
        """Get SKU-level analytics and trends"""
        if not sku_id or not store_id:
            return {}
        
        # Generate analytics data
        base_demand = self._get_base_demand(sku_id, store_id)
        dates = self._generate_dates(days)
        sales = self._generate_sales_data(base_demand, dates, sku_id, store_id)
        
        # Calculate metrics
        total_sales = sum(sales)
        avg_daily_sales = total_sales / len(sales)
        max_sales = max(sales)
        min_sales = min(sales)
        
        # Calculate trend
        if len(sales) >= 7:
            recent_avg = sum(sales[-7:]) / 7
            trend = ((recent_avg - avg_daily_sales) / avg_daily_sales) * 100
        else:
            trend = 0
        
        return {
            'sku_id': sku_id,
            'store_id': store_id,
            'total_sales': total_sales,
            'avg_daily_sales': round(avg_daily_sales, 2),
            'max_daily_sales': max_sales,
            'min_daily_sales': min_sales,
            'trend_percentage': round(trend, 2),
            'trend_direction': 'up' if trend > 0 else 'down' if trend < 0 else 'stable',
            'sku_info': self.sku_info.get(sku_id, {}),
            'store_info': self.store_info.get(store_id, {}),
            'sales_data': {
                'dates': dates,
                'sales': sales
            }
        } 