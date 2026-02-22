#!/usr/bin/env python
"""Test remote PostgreSQL database connection"""
import psycopg2
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

def test_connection():
    """Test database connection"""
    try:
        print(f"🔗 Connecting to remote PostgreSQL...")
        print(f"   Host: {DB_HOST}")
        print(f"   User: {DB_USER}")
        print(f"   Database: {DB_NAME}")
        print(f"   Port: {DB_PORT}\n")
        
        connection = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        db_version = cursor.fetchone()
        print(f"✅ Connected successfully!")
        print(f"   Database version: {db_version[0]}\n")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        print(f"📊 Tables in database:")
        if tables:
            for table in tables:
                print(f"   • {table[0]}")
        else:
            print("   ⚠️  No tables found. Database might need initialization.")
        
        # Check user count if users table exists
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"\n👥 Users in database: {user_count}")
        except:
            pass
        
        cursor.close()
        connection.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
