import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_CUSTOMERS = 500
NUM_ORDERS = 1000
NUM_PRODUCTS = 50

print("\n" + "="*60)
print("🚀 E-Commerce Sales Analytics - Data Generation")
print("="*60)

# Generate Products Data
print("\n📦 Generating Products...")
products_data = []
product_categories = [
    'Electronics', 'Clothing', 'Home & Garden', 'Sports', 
    'Books', 'Toys', 'Food', 'Mobile Accessories'
]

for i in range(1, NUM_PRODUCTS + 1):
    category = random.choice(product_categories)
    price = round(np.random.uniform(10, 1000), 2)
    stock = random.randint(50, 500)
    products_data.append({
        'product_id': i,
        'product_name': f'{category} Product {i}',
        'category': category,
        'price': price,
        'stock_quantity': stock,
        'supplier': f'Supplier_{random.randint(1, 20)}'
    })

products_df = pd.DataFrame(products_data)
products_df.to_csv('products.csv', index=False)
print(f"✓ Generated {len(products_df)} products")

# Generate Customers Data
print("\n👥 Generating Customers...")
countries = ['USA', 'UK', 'Canada', 'Germany', 'France', 'Australia', 'India', 'Japan']
cities = {
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'UK': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow'],
    'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
    'Germany': ['Berlin', 'Munich', 'Frankfurt', 'Hamburg', 'Cologne'],
    'France': ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice'],
    'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'],
    'India': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai'],
    'Japan': ['Tokyo', 'Osaka', 'Yokohama', 'Kyoto', 'Kobe']
}

customers_data = []
for i in range(1, NUM_CUSTOMERS + 1):
    country = random.choice(countries)
    city = random.choice(cities[country])
    signup_date = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 730))
    lifetime_value = round(np.random.exponential(500) + 100, 2)
    
    customers_data.append({
        'customer_id': i,
        'customer_name': f'Customer_{i}',
        'email': f'customer_{i}@email.com',
        'country': country,
        'city': city,
        'signup_date': signup_date.strftime('%Y-%m-%d'),
        'lifetime_value': lifetime_value
    })

customers_df = pd.DataFrame(customers_data)
customers_df.to_csv('customers.csv', index=False)
print(f"✓ Generated {len(customers_df)} customers")

# Generate Orders Data
print("\n📋 Generating Orders...")
order_statuses = ['Completed', 'Pending', 'Shipped', 'Cancelled', 'Refunded']
orders_data = []

for i in range(1, NUM_ORDERS + 1):
    customer_id = random.randint(1, NUM_CUSTOMERS)
    product_id = random.randint(1, NUM_PRODUCTS)
    order_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 550))
    quantity = random.randint(1, 10)
    
    product_price = products_df[products_df['product_id'] == product_id]['price'].values[0]
    unit_price = product_price
    total_amount = round(quantity * unit_price, 2)
    
    if random.random() > 0.8:
        discount = random.uniform(0.05, 0.2)
        total_amount = round(total_amount * (1 - discount), 2)
    
    status = random.choices(order_statuses, weights=[0.60, 0.15, 0.15, 0.05, 0.05])[0]
    
    orders_data.append({
        'order_id': i,
        'customer_id': customer_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'product_id': product_id,
        'quantity': quantity,
        'unit_price': round(unit_price, 2),
        'total_amount': total_amount,
        'order_status': status
    })

orders_df = pd.DataFrame(orders_data)
orders_df.to_csv('orders.csv', index=False)
print(f"✓ Generated {len(orders_df)} orders")

print("\n" + "="*60)
print("📊 Data Generation Summary")
print("="*60)
print(f"Products: {len(products_df)} records")
print(f"Customers: {len(customers_df)} records")
print(f"Orders: {len(orders_df)} records")
print(f"Total Revenue: ${orders_df['total_amount'].sum():,.2f}")
print(f"Average Order Value: ${orders_df['total_amount'].mean():,.2f}")
print(f"Date Range: {orders_df['order_date'].min()} to {orders_df['order_date'].max()}")
print(f"\n✅ All CSV files generated successfully!")
print("="*60 + "\n")
