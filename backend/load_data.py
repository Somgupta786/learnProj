#!/usr/bin/env python
"""Load dummy data into the Render PostgreSQL database"""

import psycopg2
from datetime import datetime, timedelta
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

print('[INFO] Connecting to Render PostgreSQL database...')
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT,
    connect_timeout=15
)
cursor = conn.cursor()

try:
    # Clear existing data
    print('[INFO] Clearing existing data...')
    cursor.execute('TRUNCATE TABLE order_items CASCADE')
    cursor.execute('TRUNCATE TABLE orders CASCADE')
    cursor.execute('TRUNCATE TABLE products CASCADE')
    cursor.execute('TRUNCATE TABLE users CASCADE')
    conn.commit()
    print('[OK] Tables truncated')
    
    # Insert users
    print('[INFO] Inserting users...')
    users_data = [
        ('John Admin', 'admin@example.com', '$2b$10$YourHashedPasswordHere123456789012345678901', '9876543210', 'admin'),
        ('Jane Smith', 'jane@example.com', '$2b$10$YourHashedPasswordHere123456789012345678901', '9876543211', 'user'),
        ('Robert Johnson', 'robert@example.com', '$2b$10$YourHashedPasswordHere123456789012345678901', '9876543212', 'user'),
        ('Sarah Williams', 'sarah@example.com', '$2b$10$YourHashedPasswordHere123456789012345678901', '9876543213', 'user'),
        ('Michael Brown', 'michael@example.com', '$2b$10$YourHashedPasswordHere123456789012345678901', '9876543214', 'user'),
    ]
    
    for name, email, password, phone, role in users_data:
        cursor.execute(
            'INSERT INTO users (name, email, password, phone, role, created_at) VALUES (%s, %s, %s, %s, %s, NOW())',
            (name, email, password, phone, role)
        )
    conn.commit()
    print('[OK] Users inserted')
    
    # Insert products
    print('[INFO] Inserting products...')
    products_data = [
        ('Wireless Headphones', 'High-quality wireless headphones with noise cancellation and 30-hour battery life', 129.99, 50, 'Electronics', 'https://via.placeholder.com/300?text=Wireless+Headphones'),
        ('USB-C Cable (2m)', 'Durable USB-C charging and data transfer cable, supports fast charging', 15.99, 200, 'Electronics', 'https://via.placeholder.com/300?text=USB-C+Cable'),
        ('Portable Power Bank', '20000mAh power bank with dual USB ports and LED display', 39.99, 75, 'Electronics', 'https://via.placeholder.com/300?text=Power+Bank'),
        ('Bluetooth Speaker', 'Waterproof portable Bluetooth speaker with 12-hour battery', 59.99, 40, 'Electronics', 'https://via.placeholder.com/300?text=Bluetooth+Speaker'),
        ('USB Hub (7-in-1)', 'Multi-port USB hub with HDMI, SD card reader, and 100W power delivery', 49.99, 60, 'Electronics', 'https://via.placeholder.com/300?text=USB+Hub'),
        ('Cotton T-Shirt', 'Premium quality 100% cotton t-shirt, comfortable and durable', 24.99, 150, 'Clothing', 'https://via.placeholder.com/300?text=Cotton+T-Shirt'),
        ('Denim Jeans', 'Classic blue denim jeans with stretch fit for comfort', 69.99, 100, 'Clothing', 'https://via.placeholder.com/300?text=Denim+Jeans'),
        ('Running Shoes', 'Lightweight running shoes with cushioned sole and breathable mesh', 89.99, 80, 'Clothing', 'https://via.placeholder.com/300?text=Running+Shoes'),
        ('Winter Jacket', 'Warm winter jacket with water-resistant and insulated lining', 149.99, 40, 'Clothing', 'https://via.placeholder.com/300?text=Winter+Jacket'),
        ('Cotton Socks Bundle', 'Pack of 5 pairs of premium cotton socks', 19.99, 200, 'Clothing', 'https://via.placeholder.com/300?text=Socks+Bundle'),
        ('Python Programming Guide', 'Comprehensive guide to Python programming for beginners to advanced', 34.99, 120, 'Books', 'https://via.placeholder.com/300?text=Python+Guide'),
        ('Web Development Basics', 'Learn HTML, CSS, and JavaScript from scratch', 29.99, 90, 'Books', 'https://via.placeholder.com/300?text=Web+Dev+Basics'),
        ('Data Science Handbook', 'Complete handbook on data analysis, machine learning, and visualization', 44.99, 60, 'Books', 'https://via.placeholder.com/300?text=Data+Science'),
        ('Cloud Computing Essentials', 'AWS, Azure, and Google Cloud essentials for cloud engineers', 39.99, 70, 'Books', 'https://via.placeholder.com/300?text=Cloud+Computing'),
        ('Artificial Intelligence 101', 'Introduction to AI, machine learning, and neural networks', 49.99, 50, 'Books', 'https://via.placeholder.com/300?text=AI+101'),
        ('LED Desk Lamp', 'Adjustable LED desk lamp with USB charging port and touch control', 35.99, 45, 'Home', 'https://via.placeholder.com/300?text=LED+Lamp'),
        ('Cushion Set (4pcs)', 'Decorative cushions set for sofa, waterproof and machine washable', 59.99, 30, 'Home', 'https://via.placeholder.com/300?text=Cushion+Set'),
        ('Wall Clock', 'Modern minimalist wall clock with silent movement mechanism', 24.99, 85, 'Home', 'https://via.placeholder.com/300?text=Wall+Clock'),
        ('Door Mat', 'Non-slip welcome door mat, durable and easy to clean', 14.99, 150, 'Home', 'https://via.placeholder.com/300?text=Door+Mat'),
        ('Storage Organizer', 'Multi-compartment storage organizer for home and office use', 29.99, 60, 'Home', 'https://via.placeholder.com/300?text=Storage+Organizer'),
    ]
    
    for name, desc, price, stock, category, image_url in products_data:
        cursor.execute(
            'INSERT INTO products (name, description, price, stock, category, image_url, created_at) VALUES (%s, %s, %s, %s, %s, %s, NOW())',
            (name, desc, price, stock, category, image_url)
        )
    conn.commit()
    print(f'[OK] {len(products_data)} products inserted')
    
    # Get actual user IDs
    cursor.execute('SELECT id FROM users ORDER BY id')
    user_ids = [row[0] for row in cursor.fetchall()]
    print(f'[INFO] User IDs in database: {user_ids}')
    
    # Insert orders with correct user IDs
    print('[INFO] Inserting orders...')
    orders_data = [
        (user_ids[1], 229.97, 'delivered', '123 Main Street, New York, NY 10001'),  # Jane Smith
        (user_ids[2], 179.98, 'shipped', '456 Oak Avenue, Los Angeles, CA 90028'),   # Robert Johnson
        (user_ids[3], 349.97, 'processing', '789 Pine Road, Chicago, IL 60601'),     # Sarah Williams
        (user_ids[4], 89.98, 'pending', '321 Elm Street, Houston, TX 77001'),        # Michael Brown
        (user_ids[1], 139.98, 'delivered', '123 Main Street, New York, NY 10001'),   # Jane Smith
        (user_ids[2], 269.97, 'delivered', '456 Oak Avenue, Los Angeles, CA 90028'), # Robert Johnson
    ]
    
    for user_id, total, status, address in orders_data:
        cursor.execute(
            'INSERT INTO orders (user_id, total_amount, status, shipping_address, created_at) VALUES (%s, %s, %s, %s, NOW())',
            (user_id, total, status, address)
        )
    conn.commit()
    print(f'[OK] {len(orders_data)} orders inserted')
    
    # Verify data
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM products')
    product_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM orders')
    order_count = cursor.fetchone()[0]
    
    print(f'[OK] Data loaded successfully!')
    print(f'     - Users: {user_count}')
    print(f'     - Products: {product_count}')
    print(f'     - Orders: {order_count}')
    print('[OK] Database is ready!')
    
except Exception as e:
    print(f'[ERROR] {str(e)}')
    import traceback
    traceback.print_exc()
    
finally:
    cursor.close()
    conn.close()
