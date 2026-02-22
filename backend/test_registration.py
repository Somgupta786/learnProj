#!/usr/bin/env python
"""Test script to verify registration endpoint works"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_registration():
    """Test user registration"""
    payload = {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "password123",
        "phone": "555-1234"
    }
    
    print("Testing registration endpoint...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=payload,
            timeout=5
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code in [200, 201]:
            print("\n✅ Registration successful!")
            return True
        else:
            print(f"\n❌ Registration failed: {response.json().get('detail', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def test_login():
    """Test user login"""
    print("\n\nTesting login endpoint...")
    payload = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=payload,
            timeout=5
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("\n✅ Login successful!")
            return True
        else:
            print(f"\n❌ Login failed: {response.json().get('detail', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING REGISTRATION AND LOGIN ENDPOINTS")
    print("=" * 60 + "\n")
    
    reg_result = test_registration()
    login_result = test_login()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Registration: {'✅ PASS' if reg_result else '❌ FAIL'}")
    print(f"Login: {'✅ PASS' if login_result else '❌ FAIL'}")
