#!/usr/bin/env python
"""Test login flow manually"""
import sys
sys.path.insert(0, '.')

from db.user_db import UserDB
from utils.helpers import create_access_token

print("Testing login flow...")

# Step 1: Get user
email = 'admin@example.com'
password = 'admin123'

print(f"\n1. Getting user: {email}")
user = UserDB.get_user_by_email(email)
if user:
    print("   ✅ User found")
else:
    print("   ❌ User not found")
    sys.exit(1)

# Step 2: Verify password
print(f"\n2. Verifying password")
valid = UserDB.verify_password(password, user['password'])
print(f"   Password valid: {valid}")
if not valid:
    sys.exit(1)

# Step 3: Create token
print(f"\n3. Creating token")
try:
    token = create_access_token(user["id"], user["role"])
    print(f"   ✅ Token created: {token[:20]}...")
except Exception as e:
    print(f"   ❌ Token creation failed: {e}")
    sys.exit(1)

# Step 4: Build response
print(f"\n4. Building response")
try:
    response = {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "phone": user.get("phone"),
            "role": user["role"],
            "created_at": str(user.get("created_at")) if user.get("created_at") else None
        }
    }
    print(f"   ✅ Response built successfully")
    print(f"   User role in response: {response['user']['role']}")
except Exception as e:
    print(f"   ❌ Response building failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print(f"\n✅ Login flow complete!")
print(f"User: {response['user']['name']} ({response['user']['role']})")
