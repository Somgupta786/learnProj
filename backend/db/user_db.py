import mysql.connector
from typing import Optional, Tuple
from config.database import get_db_connection, close_db_connection
from utils.validators import validate_user_email, validate_password
import bcrypt

class UserDB:
    @staticmethod
    def create_user(name: str, email: str, password: str, phone: str = None, role: str = "user") -> dict:
        """Create a new user"""
        if not validate_user_email(email):
            raise ValueError("Invalid email format")
        
        if not validate_password(password):
            raise ValueError("Password must be at least 6 characters")

        # Check if email exists
        if UserDB.get_user_by_email(email):
            raise ValueError("Email already registered")

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = "INSERT INTO users (name, email, password, phone, role, created_at) VALUES (%s, %s, %s, %s, %s, NOW())"
            cursor.execute(query, (name, email, hashed_password.decode('utf-8'), phone, role))
            conn.commit()
            user_id = cursor.lastrowid
            return {"id": user_id, "name": name, "email": email, "phone": phone, "role": role}
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def get_user_by_email(email: str) -> Optional[dict]:
        """Get user by email"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[dict]:
        """Get user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            query = "SELECT id, name, email, phone, role, created_at FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def get_all_users(limit: int = 10, offset: int = 0) -> Tuple[list, int]:
        """Get all users with pagination"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            query = "SELECT id, name, email, phone, role, created_at FROM users LIMIT %s OFFSET %s"
            cursor.execute(query, (limit, offset))
            users = cursor.fetchall()

            count_query = "SELECT COUNT(*) as total FROM users"
            cursor.execute(count_query)
            total = cursor.fetchone()["total"]

            return users, total
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def update_user(user_id: int, name: str = None, phone: str = None) -> Optional[dict]:
        """Update user profile"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if name:
                query = "UPDATE users SET name = %s WHERE id = %s"
                cursor.execute(query, (name, user_id))
            
            if phone:
                query = "UPDATE users SET phone = %s WHERE id = %s"
                cursor.execute(query, (phone, user_id))

            conn.commit()
            return UserDB.get_user_by_id(user_id)
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
