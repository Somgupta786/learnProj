#!/usr/bin/env python
"""Script to import schema and dummy data into the database (PostgreSQL)"""
import psycopg2
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def create_schema():
    """Create database schema"""
    try:
        db_config = {
            'host': os.getenv("DB_HOST", "localhost"),
            'user': os.getenv("DB_USER", "postgres"),
            'password': os.getenv("DB_PASSWORD", ""),
            'database': os.getenv("DB_NAME", "ecommerce_db"),
            'port': os.getenv("DB_PORT", "5432")
        }
        
        print("🔗 Connecting to database...")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        print("✅ Connected successfully!\n")
        
        # Read and import schema
        print("📂 Reading SCHEMA.sql...")
        with open('SCHEMA.sql', 'r', encoding='utf-8') as f:
            schema_script = f.read()
        
        print("⏳ Creating tables...\n")
        
        for statement in schema_script.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                cursor.execute(statement)
        
        conn.commit()
        print("✅ Schema created successfully!\n")
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Schema creation error: {e}")
        return False

def import_dummy_data():
    """Read and execute SQL file"""
    try:
        db_config = {
            'host': os.getenv("DB_HOST", "localhost"),
            'user': os.getenv("DB_USER", "postgres"),
            'password': os.getenv("DB_PASSWORD", ""),
            'database': os.getenv("DB_NAME", "ecommerce_db"),
            'port': os.getenv("DB_PORT", "5432")
        }
        
        print("🔗 Connecting to database...")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        print("✅ Connected successfully!\n")
        
        # Read SQL file
        print("📂 Reading DUMMY_DATA.sql...")
        with open('DUMMY_DATA.sql', 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
        
        # Split and execute statements
        statements = sql_script.split(';')
        executed_count = 0
        
        print("⏳ Importing data...\n")
        
        for statement in statements:
            statement = statement.strip()
            # Skip empty lines and comments
            if statement and not statement.startswith('--') and len(statement.split()) > 0:
                try:
                    cursor.execute(statement)
                    executed_count += 1
                except Exception as e:
                    if 'is not valid' not in str(e) and 'You have an error' not in str(e):
                        print(f"  ⚠️  Statement: {statement[:60]}... - Error: {e}")

        
        conn.commit()
        
        # Verify data
        print("\n✅ Data imported! Verifying...\n")
        
        cursor.execute("SELECT COUNT(*) as count FROM users")
        users_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) as count FROM products")
        products_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) as count FROM orders")
        orders_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) as count FROM order_items")
        order_items_count = cursor.fetchone()[0]
        
        print("📊 DATABASE SUMMARY:")
        print(f"  ✅ Users:       {users_count}")
        print(f"  ✅ Products:    {products_count}")
        print(f"  ✅ Orders:      {orders_count}")
        print(f"  ✅ Order Items: {order_items_count}")
        
        print("\n🎉 Dummy data imported successfully!")
        print("\n📝 TEST ACCOUNTS:")
        print("  Admin:   admin@example.com / admin123")
        print("  User:    jane@example.com / admin123")
        print("  User:    robert@example.com / admin123")
        print("  User:    sarah@example.com / admin123")
        print("  User:    michael@example.com / admin123")
        
        return True
        
    except psycopg2.Error as err:
        print(f"\n❌ Database error: {err}")
        return False
    except FileNotFoundError:
        print("\n❌ DUMMY_DATA.sql file not found in current directory")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    print("=" * 50)
    print("E-COMMERCE DATABASE SETUP (PostgreSQL)")
    print("=" * 50 + "\n")
    
    # Step 1: Create schema
    if not create_schema():
        sys.exit(1)
    
    # Step 2: Import dummy data
    success = import_dummy_data()
    sys.exit(0 if success else 1)
