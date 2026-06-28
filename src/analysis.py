"""
Analysis Module
Core analysis functions for e-commerce analytics
"""

import pandas as pd
import numpy as np
from datetime import datetime


class ECommerceAnalyzer:
    """Analyzer for e-commerce data"""
    
    def __init__(self, customers_df: pd.DataFrame, orders_df: pd.DataFrame, products_df: pd.DataFrame):
        self.customers = customers_df.copy()
        self.orders = orders_df.copy()
        self.products = products_df.copy()
    
    def rfm_analysis(self, completed_only: bool = True) -> pd.DataFrame:
        """Perform RFM (Recency, Frequency, Monetary) analysis"""
        orders = self.orders.copy()
        
        if completed_only:
            orders = orders[orders['order_status'].isin(['Completed', 'Shipped'])]
        
        today = orders['order_date'].max()
        rfm = orders.groupby('customer_id').agg({
            'order_date': lambda x: (today - x.max()).days,
            'order_id': 'count',
            'total_amount': 'sum'
        }).rename(columns={
            'order_date': 'recency',
            'order_id': 'frequency',
            'total_amount': 'monetary'
        })
        
        rfm = rfm.merge(self.customers[['customer_id', 'customer_name']], 
                       left_index=True, right_on='customer_id')
        
        rfm['segment'] = rfm.apply(self._assign_segment, axis=1)
        
        return rfm.sort_values('monetary', ascending=False)
    
    def _assign_segment(self, row) -> str:
        """Assign customer segment based on RFM scores"""
        if row['recency'] <= 30 and row['frequency'] >= 3 and row['monetary'] >= 500:
            return 'Champions'
        elif row['recency'] <= 90 and row['frequency'] >= 2:
            return 'Loyal'
        elif row['frequency'] == 1:
            return 'Potential'
        elif row['recency'] > 180:
            return 'At-Risk'
        else:
            return 'Moderate'
    
    def sales_trend_analysis(self) -> pd.DataFrame:
        """Analyze sales trends over time"""
        orders = self.orders[self.orders['order_status'].isin(['Completed', 'Shipped'])].copy()
        orders['month'] = pd.to_datetime(orders['order_date']).dt.to_period('M')
        
        trend = orders.groupby('month').agg({
            'order_id': 'count',
            'total_amount': ['sum', 'mean']
        }).round(2)
        
        return trend
    
    def product_performance(self) -> pd.DataFrame:
        """Analyze product performance"""
        orders = self.orders[self.orders['order_status'].isin(['Completed', 'Shipped'])].copy()
        
        performance = orders.merge(self.products, on='product_id').groupby(
            ['product_id', 'product_name', 'category']
        ).agg({
            'order_id': 'count',
            'total_amount': ['sum', 'mean']
        }).round(2)
        
        return performance.sort_values('total_amount', ascending=False)
    
    def geographic_analysis(self) -> pd.DataFrame:
        """Analyze geographic performance"""
        orders = self.orders[self.orders['order_status'].isin(['Completed', 'Shipped'])].copy()
        
        geo = orders.merge(self.customers[['customer_id', 'country', 'city']], on='customer_id').groupby(
            ['country', 'city']
        ).agg({
            'order_id': 'count',
            'total_amount': ['sum', 'mean']
        }).round(2)
        
        return geo.sort_values('total_amount', ascending=False)
    
    def customer_lifetime_value(self) -> pd.DataFrame:
        """Calculate customer lifetime value"""
        orders = self.orders[self.orders['order_status'].isin(['Completed', 'Shipped'])]
        
        clv = orders.groupby('customer_id').agg({
            'order_id': 'count',
            'total_amount': 'sum'
        }).rename(columns={
            'order_id': 'num_orders',
            'total_amount': 'total_spent'
        })
        
        clv = clv.merge(self.customers[['customer_id', 'customer_name', 'country']], 
                       left_index=True, right_on='customer_id')
        
        return clv.sort_values('total_spent', ascending=False)
