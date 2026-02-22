#!/usr/bin/env python
"""Script to fix user passwords with proper bcrypt hashing"""
import mysql.connector
from bcrypt import hashpw, gensalt

def fix_user_passwords():
    """Update all test user passwords with proper bcrypt hashes"""
    try:
        # Generate proper bcrypt hash for "admin123"
        password = "admin123"
        hashed_password = hashpw(password.encode('utf-8'), gensalt(rounds=10)).decode('utf-8')
        
        print(f"🔐 Password: {password}")
        print(f"✅ Bcrypt Hash: {hashed_password}\n")
        
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Som@7866',
            'database': 'ecommerce_db'
        }
        
        print("🔗 Connecting to database...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("✅ Connected successfully!\n")
        
        # Update all user passwords
        print("🔄 Updating user passwords...\n")
        
        cursor.execute("UPDATE users SET password = %s", (hashed_password,))
        conn.commit()
        
        # Verify
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()
        
        print("✅ Password updated for all users:\n")
        for user_id, name, email in users:
            print(f"  • {email} ({name})")
        
        print("\n" + "=" * 60)
        print("✅ PASSWORD FIX COMPLETE!")
        print("=" * 60)
        print(f"\n📝 All users can now login with password: {password}\n")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    fix_user_passwords()
