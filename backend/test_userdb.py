#!/usr/bin/env python
"""Test UserDB functions directly"""
from db.user_db import UserDB

print('=' * 60)
print('TESTING USER DATABASE FUNCTIONS')
print('=' * 60)

# Test 1: Get user by email
print('\n1. Getting user by email...')
user = UserDB.get_user_by_email('admin@example.com')
if user:
    print(f'   ✅ User found: {user.get("name")} ({user.get("email")})')
    print(f'   Password hash: {user.get("password")[:20]}...')
else:
    print('   ❌ User not found')

# Test 2: Verify password
if user:
    print('\n2. Testing password verification...')
    test_password = 'admin123'
    result = UserDB.verify_password(test_password, user['password'])
    print(f'   Password: {test_password}')
    print(f'   Stored hash: {user["password"][:30]}...')
    print(f'   ✅ Match: {result}' if result else f'   ❌ No match')
    
    if not result:
        # Debug: let's see what bcrypt thinks
        import bcrypt
        try:
            # Try direct bcrypt verification
            bytes_hash = user['password'].encode('utf-8')
            bytes_pwd = test_password.encode('utf-8')
            result2 = bcrypt.checkpw(bytes_pwd, bytes_hash)
            print(f'   Direct bcrypt test: {result2}')
        except Exception as e:
            print(f'   Error: {e}')
