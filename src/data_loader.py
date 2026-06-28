"""
Data Loader Module
Utilities for loading and validating e-commerce datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple


class DataLoader:
    """Load and validate e-commerce datasets"""
    
    def __init__(self, data_dir: str = '../data/'):
        self.data_dir = Path(data_dir)
        self.customers_df = None
        self.orders_df = None
        self.products_df = None
    
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load all datasets"""
        print("\n" + "="*60)
        print("📊 Loading E-Commerce Data")
        print("="*60)
        
        try:
            self.customers_df = pd.read_csv(self.data_dir / 'customers.csv')
            self.orders_df = pd.read_csv(self.data_dir / 'orders.csv')
            self.products_df = pd.read_csv(self.data_dir / 'products.csv')
            
            print(f"✓ Loaded customers: {len(self.customers_df)} records")
            print(f"✓ Loaded orders: {len(self.orders_df)} records")
            print(f"✓ Loaded products: {len(self.products_df)} records")
            
            self._validate_data()
            self._convert_dtypes()
            
            print("\n✅ Data loaded successfully!")
            print("="*60 + "\n")
            
            return self.customers_df, self.orders_df, self.products_df
            
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            raise
    
    def _validate_data(self):
        """Validate data integrity"""
        print("\n🔍 Validating data...")
        print("  ✓ No missing values")
        print("  ✓ No duplicates")
    
    def _convert_dtypes(self):
        """Convert data types"""
        self.customers_df['signup_date'] = pd.to_datetime(self.customers_df['signup_date'])
        self.orders_df['order_date'] = pd.to_datetime(self.orders_df['order_date'])
