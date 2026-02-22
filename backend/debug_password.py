#!/usr/bin/env python
"""Debug admin login - test password hash"""
import bcrypt
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
import psycopg2

# Connect to database
conn = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT
)
cursor = conn.cursor()

# Get admin user
cursor.execute("SELECT id, email, password FROM users WHERE email = 'admin@example.com'")
result = cursor.fetchone()
cursor.close()
conn.close()

if result:
    user_id, email, stored_hash = result
    print('=' * 60)
    print('ADMIN PASSWORD DEBUG')
    print('=' * 60)
    print(f'\nUser ID: {user_id}')
    print(f'Email: {email}')
    print(f'Stored hash: {stored_hash[:50]}...')
    print(f'Hash length: {len(stored_hash)}')
    
    # Try to verify password
    test_password = 'admin123'
    print(f'\nTesting password: {test_password}')
    
    try:
        # This is what the code does
        result = bcrypt.checkpw(test_password.encode('utf-8'), stored_hash.encode('utf-8'))
        print(f'✅ Password match: {result}')
    except Exception as e:
        print(f'❌ Error during verification: {e}')
        print(f'   Error type: {type(e).__name__}')
        
        # Try alternative
        try:
            print('\nTrying alternative method...')
            result = bcrypt.checkpw(test_password.encode('utf-8'), stored_hash)
            print(f'   Alternative worked: {result}')
        except Exception as e2:
            print(f'   Alternative also failed: {e2}')
