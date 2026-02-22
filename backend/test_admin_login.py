#!/usr/bin/env python
"""Test admin login flow"""
import requests

print('=' * 60)
print('TESTING ADMIN LOGIN FLOW')
print('=' * 60)

# Step 1: Login
login_data = {'email': 'admin@example.com', 'password': 'admin123'}
print('\n1. Logging in: admin@example.com')

resp = requests.post('http://localhost:8000/api/auth/login', json=login_data)
print(f'   Status: {resp.status_code}')

if resp.status_code == 200:
    data = resp.json()
    print('   Login successful!')
    
    user = data.get('user', {})
    print('\n   User Details:')
    print(f'   - Name: {user.get("name")}')
    print(f'   - Email: {user.get("email")}')
    print(f'   - Role: {user.get("role")}')
    print(f'   - ID: {user.get("id")}')
    
    if user.get('role') == 'admin':
        print('\n✅ SUCCESS: User IS ADMIN')
        print('   Should have access to admin panel')
    else:
        print(f'\n❌ PROBLEM: User role is "{user.get("role")}", not "admin"!')
else:
    print(f'❌ Login failed: {resp.json()}')

# Check database role
print('\n' + '=' * 60)
print('CHECKING DATABASE')
print('=' * 60)

from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
import psycopg2

conn = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT
)
cursor = conn.cursor()
cursor.execute("SELECT id, name, email, role FROM users WHERE email = 'admin@example.com'")
admin_user = cursor.fetchone()
cursor.close()
conn.close()

if admin_user:
    print(f'\nAdmin user in database:')
    print(f'  ID: {admin_user[0]}')
    print(f'  Name: {admin_user[1]}')
    print(f'  Email: {admin_user[2]}')
    print(f'  Role: {admin_user[3]}')
    
    if admin_user[3] == 'admin':
        print('\n✅ Database role is correct: admin')
    else:
        print(f'\n❌ Database role is: {admin_user[3]} (should be: admin)')
