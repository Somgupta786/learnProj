#!/usr/bin/env python
"""Script to set up PostgreSQL database schema and import dummy data"""
import psycopg2
from psycopg2 import Error
import sys

def setup_database():
    """Create and populate database"""
    try:
        # First, connect to default postgres database to create new database
        db_config_root = {
            'host': 'localhost',
            'user': 'postgres',
            'password': 'Sh@250704',
            'database': 'postgres'
        }
        
        print("=" * 60)
        print("E-COMMERCE DATABASE SETUP (PostgreSQL)")
        print("=" * 60 + "\n")
        
        print("🔗 Connecting to PostgreSQL server...")
        conn = psycopg2.connect(**db_config_root)
        conn.autocommit = True
        cursor = conn.cursor()
        print("✅ Connected successfully!\n")
        
        # Create database if not exists
        print("🗄️  Creating database...")
        cursor.execute("CREATE DATABASE ecommerce_db")
        print("✅ Database created\n")
        cursor.close()
        conn.close()
        
        # Now connect to the specific database
        db_config = {
            'host': 'localhost',
            'user': 'postgres',
            'password': 'Sh@250704',
            'database': 'ecommerce_db'
        }
        
        print("🔗 Connecting to ecommerce_db...")
        conn = psycopg2.connect(**db_config)
        conn.autocommit = False
        cursor = conn.cursor()
        print("✅ Connected to ecommerce_db!\n")
        
        # Step 1: Create tables
        print("📊 Creating tables...\n")
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                role VARCHAR(50) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  ✅ users table created")
        
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                stock INT NOT NULL DEFAULT 0,
                category VARCHAR(100),
                image_url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  ✅ products table created")
        
        # Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                total_amount DECIMAL(10, 2) NOT NULL,
                status VARCHAR(50) DEFAULT 'pending',
                shipping_address TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  ✅ orders table created")
        
        # Order items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
                product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                quantity INT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  ✅ order_items table created\n")
        
        conn.commit()
        
        # Clear existing data first
        print("🧹 Clearing existing data...\n")
        cursor.execute("TRUNCATE TABLE order_items, orders, products, users CASCADE")
        conn.commit()
        
        # Step 2: Insert users
        print("👥 Inserting users...\n")
        
        users_data = [
            ('John Admin', 'admin@example.com', '$2b$10$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW', '9876543210', 'admin'),
            ('Jane Smith', 'jane@example.com', '$2b$10$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW', '9876543211', 'user'),
            ('Robert Johnson', 'robert@example.com', '$2b$10$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW', '9876543212', 'user'),
            ('Sarah Williams', 'sarah@example.com', '$2b$10$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW', '9876543213', 'user'),
            ('Michael Brown', 'michael@example.com', '$2b$10$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW', '9876543214', 'user'),
        ]
        
        for user in users_data:
            cursor.execute(
                "INSERT INTO users (name, email, password, phone, role) VALUES (%s, %s, %s, %s, %s)",
                user
            )
        
        conn.commit()
        print(f"  ✅ {len(users_data)} users inserted\n")
        
        # Step 3: Insert products
        print("📦 Inserting products...\n")
        
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
        
        for product in products_data:
            cursor.execute(
                "INSERT INTO products (name, description, price, stock, category, image_url) VALUES (%s, %s, %s, %s, %s, %s)",
                product
            )
        
        conn.commit()
        print(f"  ✅ {len(products_data)} products inserted\n")
        
        # Step 4: Insert orders
        print("📋 Inserting orders...\n")
        
        orders_data = [
            (2, 229.97, 'delivered', '123 Main Street, New York, NY 10001'),
            (3, 179.98, 'shipped', '456 Oak Avenue, Los Angeles, CA 90028'),
            (4, 349.97, 'processing', '789 Pine Road, Chicago, IL 60601'),
            (5, 89.98, 'pending', '321 Elm Street, Houston, TX 77001'),
            (2, 139.98, 'delivered', '123 Main Street, New York, NY 10001'),
            (3, 269.97, 'delivered', '456 Oak Avenue, Los Angeles, CA 90028'),
        ]
        
        for order in orders_data:
            cursor.execute(
                "INSERT INTO orders (user_id, total_amount, status, shipping_address) VALUES (%s, %s, %s, %s)",
                order
            )
        
        conn.commit()
        print(f"  ✅ {len(orders_data)} orders inserted\n")
        
        # Step 5: Insert order items
        print("🛒 Inserting order items...\n")
        
        order_items_data = [
            (1, 1, 1, 129.99),
            (1, 3, 1, 39.99),
            (1, 2, 1, 15.99),
            (2, 6, 2, 24.99),
            (2, 10, 1, 19.99),
            (2, 11, 1, 34.99),
            (3, 8, 1, 89.99),
            (3, 9, 1, 149.99),
            (3, 4, 1, 59.99),
            (4, 16, 1, 24.99),
            (4, 15, 1, 29.99),
            (4, 2, 1, 15.99),
            (5, 7, 1, 69.99),
            (5, 12, 1, 29.99),
            (5, 2, 1, 15.99),
            (5, 3, 1, 24.01),
            (6, 7, 1, 69.99),
            (6, 13, 1, 44.99),
            (6, 16, 1, 35.99),
            (6, 19, 1, 14.99),
            (6, 5, 1, 49.99),
        ]
        
        for item in order_items_data:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                item
            )
        
        conn.commit()
        print(f"  ✅ {len(order_items_data)} order items inserted\n")
        
        # Step 6: Verify data
        print("=" * 60)
        print("✅ DATABASE SETUP COMPLETE!")
        print("=" * 60 + "\n")
        
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        orders_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM order_items")
        order_items_count = cursor.fetchone()[0]
        
        print("📊 DATABASE SUMMARY:")
        print(f"  ✅ Users:        {users_count}")
        print(f"  ✅ Products:     {products_count}")
        print(f"  ✅ Orders:       {orders_count}")
        print(f"  ✅ Order Items:  {order_items_count}\n")
        
        print("📝 TEST ACCOUNTS (Password: admin123 for all):")
        print("  • admin@example.com (Admin role)")
        print("  • jane@example.com")
        print("  • robert@example.com")
        print("  • sarah@example.com")
        print("  • michael@example.com\n")
        
        print("🚀 Ready to test the application!")
        print("=" * 60 + "\n")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Error as err:
        print(f"\n❌ Database error: {err}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = setup_database()
    sys.exit(0 if success else 1)
