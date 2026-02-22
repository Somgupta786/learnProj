#!/usr/bin/env python
"""Fix user passwords with real bcrypt hashes"""
import bcrypt
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
import psycopg2

print('=' * 60)
print('FIXING USER PASSWORDS')
print('=' * 60)

# Generate bcrypt hash for "admin123"
test_password = "admin123"
hashed_password = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())
hashed_str = hashed_password.decode('utf-8')

print(f'\nPassword: {test_password}')
print(f'Bcrypt hash: {hashed_str}')

# Connect to database
conn = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT
)
cursor = conn.cursor()

# Update all user passwords
cursor.execute("UPDATE users SET password = %s", (hashed_str,))
conn.commit()

# Verify
cursor.execute("SELECT id, name, email FROM users")
users = cursor.fetchall()

print(f'\n✅ Updated {len(users)} user password(s)')
print('\nUsers with reset password:')
for user_id, name, email in users:
    print(f'  • {email} ({name})')

print(f'\n✅ All users can now login with password: {test_password}')

cursor.close()
conn.close()
